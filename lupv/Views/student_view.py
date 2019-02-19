from PyQt5.QtWidgets import QWidget, QTreeWidgetItem
from PyQt5.QtGui import QBrush, QColor

from Controllers.student_controller import StudentController
from Views.student_window import Ui_Form


class StudentView(QWidget, Ui_Form):
    def __init__(self, model, controller, student_dir):
        super().__init__()
        self.setupUi(self)
        self._student_dir = student_dir
        self._model = model
        self._controller = controller
        self._student_ctrl = StudentController(model, controller, student_dir)

        self.setWindowTitle(student_dir)

        self.display_logs()
        self.display_files()
        self.log_tw.itemSelectionChanged.connect(self.selection_changed)
        self.close_btn.clicked.connect(self.close)

    def get_selected_sha(self):
        items = self.log_tw.selectedItems()
        if items:
            sha = items[0].text(2)
        return sha

    def display_logs(self):
        """Display log to log_QTreeWidget."""
        logs = self._student_ctrl.read_logs()
        for l in logs:
            QTreeWidgetItem(
                self.log_tw,
                [str(l.relative_datetime),
                 str(l.datetime),
                 str(l.sha)])

    def display_diff(self, sha):
        """Display diff to diff_QPlainTextEdit."""
        student_repo = self._student_ctrl.get_student_repo()
        student_path = self._student_ctrl.get_student_path()

        selected_file = self.get_selected_file()
        if not selected_file:
            selected_file = None

        first_rec_sha = self._controller.get_first_rec_sha(student_path)
        diff = student_repo.git.diff(first_rec_sha, sha, selected_file)
        self.diff_pte.setPlainText(diff)

    def display_files(self):
        """Display file to file_QTreeWidget."""
        student_dir = self._student_ctrl.get_student_path()
        files = self._controller.get_files(student_dir)
        for f in files:
            QTreeWidgetItem(self.file_tw, [f])

    def get_selected_file(self):
        """Return selected file in file_QTreeWidget."""
        items = self.file_tw.selectedItems()
        if items:
            selected_file = items[0].text(0)
            return selected_file

    def display_windows(self, sha):
        self.all_windows_tw.clear()

        focused_window = self._student_ctrl.read_focused_window(sha)
        focused_row = QTreeWidgetItem(self.all_windows_tw, [focused_window])

        focused_row.setForeground(0, QBrush(QColor("#41CD52")))
        windows = self._student_ctrl.read_all_windows(sha)
        for window in windows:
            if window != focused_window:
                QTreeWidgetItem(self.all_windows_tw, [window])

    def display_auth_info(self, sha):
        auth_info = self._student_ctrl.read_auth_info(sha)
        if auth_info:
            self.name_lbl.setText(auth_info[0])
            self.machine_lbl.setText(auth_info[1])
            self.ip_lbl.setText(auth_info[2])

    def selection_changed(self):
        sha = self.get_selected_sha()
        self.display_diff(sha)
        self.display_windows(sha)
        self.display_auth_info(sha)
