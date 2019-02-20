from PyQt5.QtWidgets import (QWidget, QTreeWidgetItem, QMessageBox, QMenu)
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt

from Controllers.student_controller import StudentController
from Views.student_window import Ui_Form
from Views.editdistance_view import EditDistanceView


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
        self.show_ed_btn.clicked.connect(self.show_editdistance_view)

        self.log_tw.setContextMenuPolicy(Qt.CustomContextMenu)
        self.log_tw.customContextMenuRequested.connect(self.menu_log_tw)

    def get_selected_sha(self):
        items = self.log_tw.selectedItems()
        if items:
            sha = items[0].text(2)
        return sha

    def display_logs(self):
        """Display log to log_QTreeWidget."""
        self.log_tw.hideColumn(2)  # hide SHA column (default)

        logs = self._student_ctrl.read_logs()
        for l in logs:
            QTreeWidgetItem(
                self.log_tw,
                [str(l.relative_datetime),
                 str(l.datetime),
                 str(l.sha)])

        self.log_tw.resizeColumnToContents(0)
        self.log_tw.resizeColumnToContents(1)

    def display_diff(self, sha):
        """Display diff to diff_QPlainTextEdit."""
        student_repo = self._student_ctrl.get_student_repo()

        selected_file = self.get_selected_file()
        no_file_selected_msg = 'No file selected, Please select one'
        no_file_rec_msg = 'No availibale record for {} in this period'.format(
            selected_file)

        if not selected_file:
            self.diff_pte.setPlainText(no_file_selected_msg)
        else:
            file_existp = self._student_ctrl.is_file_exist(selected_file, sha)
            if file_existp:
                current_file = student_repo.git.show('{}:{}'.format(
                    sha, selected_file))
                if current_file == '':
                    self.diff_pte.setPlainText(no_file_rec_msg)
                else:
                    self.diff_pte.setPlainText(current_file)
            else:
                pass

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

    def show_editdistance_view(self):
        selected_file = self.get_selected_file()
        editdistance_ax = self._student_ctrl.calc_editdistance_ax(
            selected_file)
        if editdistance_ax:
            self.editdistance_view = EditDistanceView(
                editdistance_ax, self._student_ctrl, self._student_dir)
            self.editdistance_view.show()
        else:
            QMessageBox.warning(self, '', 'please choose a file')

    def menu_log_tw(self, event):
        menu = QMenu(self.log_tw)
        sha_menu = menu.addMenu("SHA")
        stat_menu = menu.addMenu("Statistic")
        actionShow_sha = sha_menu.addAction('Show SHA')
        actionHide_sha = sha_menu.addAction('Hide SHA')
        actionShow_stat = stat_menu.addAction('Show stat')
        actionHide_stat = stat_menu.addAction('Hide stat')
        action = menu.exec_(self.log_tw.mapToGlobal(event))
        if action is not None:
            if action == actionShow_sha:
                self.log_tw.showColumn(2)
            elif action == actionHide_sha:
                self.log_tw.hideColumn(2)
            elif action == actionShow_stat:
                print('show stat')
            elif action == actionHide_stat:
                print('show stat')
