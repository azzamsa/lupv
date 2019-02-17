from Model.logs import Logs
from Views.student_window import Ui_Form

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem


class StudentView(QWidget, Ui_Form):

    def __init__(self, model, controller, student_dir):
        super().__init__()
        self.setupUi(self)
        self._student_dir = student_dir
        self._model = model
        self._controller = controller

        self.setWindowTitle(student_dir)

        self.display_logs()
        self.display_files()
        self.log_tw.itemSelectionChanged.connect(self.selection_changed)
        self.close_btn.clicked.connect(self.close)

    def get_student_dir(self):
        record_path = self._model.get_record_path()
        student_dir = record_path + '/' + self._student_dir
        return student_dir

    def get_student_repo(self):
        student_dir = self.get_student_dir()
        student_repo = self._controller.initialize_repo(student_dir)
        return student_repo

    def get_selected_sha(self):
        items = self.log_tw.selectedItems()
        if items:
            sha = items[0].text(3)
        return sha

    def parse_logs(self):
        """Read log form student directory"""
        student_dir = self.get_student_dir()
        recs = self._controller.get_records(student_dir)
        logs = []

        for rec in recs:
            name = rec.committer.name
            summary = rec.summary
            email = rec.committer.email
            sha = rec.hexsha
            log = Logs(name, summary, email, sha)
            logs.append(log)

        return logs

    def display_logs(self):
        """Display log to log_QTreeWidget"""
        logs = self.parse_logs()
        for l in logs:
            QTreeWidgetItem(self.log_tw,
                            [str(l.name),
                             str(l.email),
                             str(l.summary),
                             str(l.sha)])

    def display_diff(self, sha):
        """Display diff to diff_QPlainTextEdit"""
        student_dir = self.get_student_dir()
        student_repo = self.get_student_repo()

        selected_file = self.get_selected_file()
        if not selected_file:
            selected_file = None

        first_rec_sha = self._controller.get_first_record_sha(student_dir)
        diff = student_repo.git.diff(first_rec_sha, sha, selected_file)
        self.diff_pte.setPlainText(diff)

    def display_files(self):
        """Display file to file_QTreeWidget"""
        student_dir = self.get_student_dir()
        files = self._controller.get_files(student_dir)
        for f in files:
            QTreeWidgetItem(self.file_tw, [f])

    def get_selected_file(self):
        """Return selected file in file_QTreeWidget"""
        items = self.file_tw.selectedItems()
        if items:
            selected_file = items[0].text(0)
            return selected_file

    def get_all_windows(self, sha):
        student_repo = self.get_student_repo()
        diff = student_repo.git.show(sha, '.watchers/all_windows')
        diff_body = diff.splitlines()[14:]
        windows = []
        for line in diff_body:
            if line != '':
                windows.append(line)
        return windows

    def display_all_windows(self, sha):
        # clear previous items
        self.all_windows_tw.clear()  # FIXME, is it safe ?
        windows = self.get_all_windows(sha)
        for window in windows:
            QTreeWidgetItem(self.all_windows_tw, [window])

    def selection_changed(self):
        sha = self.get_selected_sha()
        self.display_diff(sha)
        self.display_all_windows(sha)
