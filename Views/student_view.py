from Model.logs import Logs
from Views.student_window import Ui_Form

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem
from PyQt5.QtGui import QTextCursor


class StudentView(QWidget, Ui_Form):

    def __init__(self, model, controller, student_dir):
        super().__init__()
        self.setupUi(self)
        self._student_dir = student_dir
        self._model = model
        self._controller = controller

        self.setWindowTitle(student_dir)

        self.populate_log()
        self.display_files()
        self.log_tw.itemSelectionChanged.connect(self.display_diff)
        self.close_btn.clicked.connect(self.close)

    def parse_logs(self):
        """Read log form student directory"""
        record_path = self._model.get_record_path()
        student_dir = record_path + '/' + self._student_dir
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

    def populate_log(self):
        """Display log to log QTreeWidget"""
        logs = self.parse_logs()
        for l in logs:
            QTreeWidgetItem(self.log_tw,
                            [str(l.name),
                             str(l.email),
                             str(l.summary),
                             str(l.sha)])

    def display_diff(self):
        """Display diff to diff QPlainTextEdit"""
        items = self.log_tw.selectedItems()
        sha = items[0].text(3)
        record_path = self._model.get_record_path()
        student_dir = record_path + '/' + self._student_dir
        first_rec_sha = self._controller.get_first_record_sha(student_dir)
        repo = self._controller.initialize_repo(student_dir)
        diff = repo.git.diff(first_rec_sha, sha)
        self.diff_pte.setPlainText(diff)

    def display_files(self):
        """Display file to file QTreeWidget"""
        record_path = self._model.get_record_path()
        student_dir = record_path + '/' + self._student_dir
        files = self._controller.get_files(student_dir)
        for f in files:
            QTreeWidgetItem(self.file_tw, [f])
