import os
from os.path import join
from Resources.theme import breeze_resources
from collections import OrderedDict

from PyQt5.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QTableWidgetItem,
    QApplication,
    QLabel,
    QMessageBox,
    QTreeWidgetItem,
)
from PyQt5.QtCore import QFile, QTextStream, Qt
from PyQt5.QtGui import QKeySequence, QBrush, QColor

from Views.main_window import Ui_MainWindow
from Controllers.student_controller import StudentController
from Views.editdistance_view import EditDistanceView


class MyDict(OrderedDict):
    def __missing__(self, key):
        val = self[key] = MyDict()
        return val


class MainView(QMainWindow, Ui_MainWindow):
    def __init__(self, model, controller):
        super().__init__()
        self._model = model
        self._controller = controller
        self.setupUi(self)

        # mainview actions
        self.actionOpen_Records.triggered.connect(self.open_records)
        self.actionOpen_Records.setShortcut(QKeySequence("Ctrl+O"))
        self.actionQuit.triggered.connect(self.quit_app)
        self.actionQuit.setShortcut(QKeySequence("Ctrl+Q"))

        self.main_tablew.clicked.connect(self.show_student_page)
        self.actionRealDate.triggered.connect(
            lambda: self.display_records(humanize=False)
        )
        self.actionRelativeDate.triggered.connect(
            lambda: self.display_records(humanize=True)
        )
        self.actionRealDate.setEnabled(False)  # default
        self.actionRelativeDate.setEnabled(False)

        # student page actions
        self.actionHide_SHA.setEnabled(False)
        self.actionShow_SHA.setEnabled(False)
        self.actionShow_stats.setEnabled(False)
        self.actionHide_stats.setEnabled(False)
        self.actionShow_Editdistance.setEnabled(False)

        self.stackedWidget.setCurrentIndex(0)
        self.to_mainview_btn.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(0)
        )

        # Toggle theme
        dark = "../lupv/Resources/theme/dark.qss"
        light = "../lupv/Resources/theme/light.qss"
        self.actionToggleDark.triggered.connect(lambda: self.toggle_theme(dark))
        self.actionToggleLight.triggered.connect(lambda: self.toggle_theme(light))
        self.toggle_theme(dark)  # default theme

        css = """
        color: white;
        font-size: 12px;
        border-radius: 20px;
        qproperty-alignment: AlignCenter;
        min-height: 25px;
        min-width: 250px;
        background: #1d2c3a;
        """

        self.main_tablew.setVisible(False)
        self.welcome_lbl = QLabel()
        self.welcome_lbl.setText("Please open records to start analyzing")
        self.welcome_lbl.setStyleSheet(css)
        self.verticalLayout.addWidget(self.welcome_lbl, alignment=Qt.AlignCenter)

        self.show()

    def quit_app(self):
        """Quit application."""
        QApplication.quit()
        self.close()

    def toggle_theme(self, path):
        """Change application theme based on theme location."""
        lupv = QApplication.instance()
        file = QFile(path)
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        lupv.setStyleSheet(stream.readAll())

    def choosedir_dialog(self, caption):
        """Prompts dialog to choose record directory."""
        options = QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        return QFileDialog.getExistingDirectory(self, caption=caption, options=options)

    def validate_path(self, path):
        """Validate chosen path.

        TODO: Move this to controller

        This is necessary because invalid path will break `read_records` and
        make application crash.
        """
        dirs = os.listdir(path)
        invalid_dirs = []
        for d in dirs:
            if not os.path.isdir(join(path, d, ".git")):
                invalid_dirs.append(d)

        msg = "Not a valid Tasks directory\n"
        details = "\nContains invalid Task:\n{}".format("\n".join(invalid_dirs))

        if len(invalid_dirs) == 0:
            return True
        elif len(invalid_dirs) <= 10:
            QMessageBox.warning(self, "", msg + details)
        else:
            QMessageBox.warning(self, "", msg + "\n\nContains many invalid Tasks")

    def save_record_path(self, record_path):
        """Save record path."""
        self._controller.save_record_path(record_path)

    def open_records(self):
        """Open records directory then display the record."""
        path = self.choosedir_dialog("Select Directory...")
        if not path:
            return None
        else:
            if not self.validate_path(path):
                return None

        self.save_record_path(path)
        self.actionRealDate.setEnabled(True)
        self.actionRelativeDate.setEnabled(True)
        self.display_records()

    def display_records(self, humanize=True):
        """Populate records."""
        recs = self._controller.read_records(humanize)
        ord_recs = MyDict()  # ordered records

        for rec in recs:
            ord_recs[rec.name]["name"] = rec.name
            ord_recs[rec.name]["nim"] = rec.nim
            ord_recs[rec.name]["record_amounts"] = rec.record_amounts
            ord_recs[rec.name]["work_duration"] = rec.work_duration
            ord_recs[rec.name]["first_record"] = rec.first_record
            ord_recs[rec.name]["last_record"] = rec.last_record

        self.main_tablew.setRowCount(0)

        for row_num, key_name in enumerate(ord_recs):
            self.main_tablew.insertRow(row_num)
            for col_num, col_key in enumerate(ord_recs[key_name]):
                tbl_item = QTableWidgetItem(str(ord_recs[key_name][col_key]))
                self.main_tablew.setItem(row_num, col_num, tbl_item)

        self.welcome_lbl.setVisible(False)
        self.main_tablew.setVisible(False)
        self.main_tablew.verticalScrollBar().setValue(0)
        self.main_tablew.resizeColumnsToContents()
        self.main_tablew.setVisible(True)

    def get_selected_student(self):
        """Return selected student from main table"""
        name = self.main_tablew.item(self.main_tablew.currentRow(), 0).text()
        nim = self.main_tablew.item(self.main_tablew.currentRow(), 1).text()
        student_dir = name + "-" + nim
        return student_dir

    def show_student_page(self):
        """Show Student Page and do initial things."""
        # named column for easier reading
        self.reldate_col = 0
        self.datetime_col = 1
        self.sha_col = 2
        self.insertions_col = 3
        self.deletions_col = 4

        self.actionHide_SHA.setEnabled(True)
        self.actionShow_SHA.setEnabled(True)
        self.actionShow_stats.setEnabled(True)
        self.actionHide_stats.setEnabled(True)
        self.actionShow_Editdistance.setEnabled(True)

        self.actionShow_Editdistance.triggered.connect(self.show_editdistance_view)
        self.actionShow_SHA.triggered.connect(lambda: self.toggle_sha(True))
        self.actionHide_SHA.triggered.connect(lambda: self.toggle_sha(False))
        self.actionShow_stats.triggered.connect(lambda: self.toogle_stats(True))
        self.actionHide_stats.triggered.connect(lambda: self.toogle_stats(False))

        student_dir = self.get_selected_student()
        self._student_ctrl = StudentController(
            self._model, self._controller, student_dir
        )

        self.log_treew.itemSelectionChanged.connect(self.selection_changed)
        self.clear_widgets()

        self.display_logs(False)
        self.display_files()
        self.stackedWidget.setCurrentIndex(1)

    def clear_widgets(self):
        """Clear all widget contents."""
        self.diff_textw.clear()
        self.log_treew.clear()
        self.file_treew.clear()
        self.windows_treew.clear()

    def get_selected_sha(self):
        """Get SHA value from log_QTreeWidget."""
        sha = 0
        items = self.log_treew.selectedItems()
        if items:
            sha = items[0].text(2)
        return sha

    def display_logs(self, complete=False):
        """Display log to log_QTreeWidget."""
        self.log_treew.clear()

        self.log_treew.hideColumn(self.sha_col)
        self.log_treew.hideColumn(self.insertions_col)
        self.log_treew.hideColumn(self.deletions_col)

        selected_file = self.get_selected_file()
        logs = self._student_ctrl.read_logs(selected_file)

        if complete:
            if selected_file:
                self.log_treew.clear()
                for l in logs:
                    QTreeWidgetItem(
                        self.log_treew,
                        [
                            str(l.relative_datetime),
                            str(l.datetime),
                            str(l.sha),
                            "{} {line}".format(
                                l.add_stats,
                                line="Line" if l.add_stats == 0 else "Lines",
                            ),
                            "{} {line}".format(
                                l.del_stats,
                                line="Line" if l.del_stats == 0 else "Lines",
                            ),
                        ],
                    )
                self.log_treew.showColumn(3)
                self.log_treew.showColumn(4)
                self.log_treew.resizeColumnToContents(3)
                self.log_treew.resizeColumnToContents(4)
            else:
                QMessageBox.warning(self, "", "please choose a file")
        else:
            for l in logs:
                QTreeWidgetItem(
                    self.log_treew, [str(l.relative_datetime), str(l.datetime), str(l.sha)]
                )

        self.log_treew.resizeColumnToContents(0)
        self.log_treew.resizeColumnToContents(1)

    def display_diff(self, sha):
        """Display diff to diff_QPlainTextEdit."""
        self.diff_textw.clear()
        student_repo = self._student_ctrl.get_student_repo()

        selected_file = self.get_selected_file()
        no_file_selected_msg = "No file selected, Please select one"
        no_file_rec_msg = "No availibale record for {} in this period".format(
            selected_file
        )

        if not selected_file:
            self.diff_textw.setPlainText(no_file_selected_msg)
        else:
            file_existp = self._student_ctrl.is_file_exist(selected_file, sha)
            if file_existp:
                current_file = student_repo.git.show("{}:{}".format(sha, selected_file))
                if current_file == "":
                    self.diff_textw.setPlainText(no_file_rec_msg)
                else:
                    self.diff_textw.setPlainText(current_file)
            else:
                pass

    def display_files(self):
        """Display file to file_QTreeWidget."""
        self.file_treew.clear()
        student_dir = self._student_ctrl.get_student_path()
        files = self._controller.get_files(student_dir)
        for f in files:
            QTreeWidgetItem(self.file_treew, [f])

    def get_selected_file(self):
        """Return selected file in file_QTreeWidget."""
        items = self.file_treew.selectedItems()
        if items:
            selected_file = items[0].text(0)
            return selected_file

    def display_windows(self, sha):
        """Display all windows and focused window from records."""
        self.windows_treew.clear()

        focused_window = self._student_ctrl.read_focused_window(sha)
        focused_row = QTreeWidgetItem(self.windows_treew, [focused_window])

        focused_row.setForeground(0, QBrush(QColor("#41CD52")))
        windows = self._student_ctrl.read_all_windows(sha)
        for window in windows:
            if window != focused_window:
                QTreeWidgetItem(self.windows_treew, [window])

    def display_auth_info(self, sha):
        """Display auth information from records."""
        auth_info = self._student_ctrl.read_auth_info(sha)
        if auth_info:
            self.name_lbl.setText(auth_info[0])
            self.machine_lbl.setText(auth_info[1])
            self.ip_lbl.setText(auth_info[2])

    def selection_changed(self):
        """Actions invoked when selection in log_QTreeWidget changed."""
        sha = self.get_selected_sha()
        if sha:
            self.display_diff(sha)
            self.display_windows(sha)
            self.display_auth_info(sha)

    def show_editdistance_view(self):
        """Open EditDistance Window"""
        student_dir = self.get_selected_student()
        selected_file = self.get_selected_file()
        if selected_file:
            editdistance_ax = self._student_ctrl.calc_editdistance_ax(selected_file)
            if editdistance_ax:
                self.editdistance_view = EditDistanceView(
                    editdistance_ax, self._student_ctrl, student_dir
                )
                self.editdistance_view.show()
        else:
            QMessageBox.warning(self, "", "Please choose a file")

    def toggle_sha(self, toogle=False):
        """Toggle the appearance of SHA columns."""
        if toogle:
            self.log_treew.showColumn(self.sha_col)
        else:
            self.log_treew.hideColumn(self.sha_col)
        for col in range(5):
            if col != 2:
                self.log_treew.resizeColumnToContents(col)

    def toogle_stats(self, toogle=False):
        """Toggle the appearance of stats columns."""
        if toogle:
            self.display_logs(True)
        else:
            self.log_treew.hideColumn(3)
            self.log_treew.hideColumn(4)
            self.log_treew.resizeColumnToContents(0)
            self.log_treew.resizeColumnToContents(1)
