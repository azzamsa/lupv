import os
from os.path import join
from Resources.theme import breeze_resources
from collections import OrderedDict

from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QTableWidgetItem,
                             QApplication, QLabel, QMessageBox,
                             QTreeWidgetItem)
from PyQt5.QtCore import QFile, QTextStream, Qt
from PyQt5.QtGui import QKeySequence, QBrush, QColor

from Views.stacked import Ui_MainWindow
from Views.student_view import StudentView
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

        self.actionOpen_Records.triggered.connect(self.open_records)
        self.actionOpen_Records.setShortcut(QKeySequence("Ctrl+O"))
        self.actionQuit.triggered.connect(self.quit_app)
        self.actionQuit.setShortcut(QKeySequence("Ctrl+Q"))

        self.tableWidget.clicked.connect(self.show_student_page)
        self.actionRealDate.triggered.connect(lambda: self.populate_records(
            humanize=False))
        self.actionRelativeDate.triggered.connect(
            lambda: self.populate_records(humanize=True))
        self.actionRealDate.setEnabled(False)  # default
        self.actionRelativeDate.setEnabled(False)

        self.stackedWidget.setCurrentIndex(0)
        self.to_mainview_btn.clicked.connect(lambda: self.stackedWidget.
                                             setCurrentIndex(0))
        # student page
        self.actionHide_SHA.setVisible(False)
        self.actionShow_SHA.setVisible(False)
        self.actionShow_stats.setVisible(False)
        self.actionHide_stats.setVisible(False)
        self.actionShow_Edit_distance.setVisible(False)

        # Toggle theme
        dark = '../lupv/Resources/theme/dark.qss'
        light = '../lupv/Resources/theme/light.qss'
        self.actionToggleDark.triggered.connect(lambda: self.toggle_theme(dark)
                                                )
        self.actionToggleLight.triggered.connect(lambda: self.toggle_theme(
            light))
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

        self.tableWidget.setVisible(False)
        self.welcome_lbl = QLabel()
        self.welcome_lbl.setText("Please open records to start analyzing")
        self.welcome_lbl.setStyleSheet(css)
        self.verticalLayout.addWidget(
            self.welcome_lbl, alignment=Qt.AlignCenter)

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
        options = (QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        return QFileDialog.getExistingDirectory(
            self, caption=caption, options=options)

    def validate_path(self, path):
        """Validate chosen path.

        This is necessary because invalid path will break `read_records` and
        make application crash.
        """
        dirs = os.listdir(path)
        invalid_dirs = []
        for d in dirs:
            if not os.path.isdir(join(path, d, '.git')):
                invalid_dirs.append(d)

        msg = 'Not a valid Tasks directory\n'
        details = '\nContains invalid Task:\n{}'.format(
            '\n'.join(invalid_dirs))

        if len(invalid_dirs) == 0:
            return True
        elif len(invalid_dirs) <= 10:
            QMessageBox.warning(self, '', msg + details)
        else:
            QMessageBox.warning(self, '',
                                msg + '\n\nContains many invalid Tasks')

    def save_record_path(self, record_path):
        """Save record path."""
        self._controller.save_record_path(record_path)

    def open_records(self):
        """Open records directory then display the record."""
        path = self.choosedir_dialog('Select Directory...')
        if not path:
            return None
        else:
            if not self.validate_path(path):
                return None

        self.save_record_path(path)
        self.actionRealDate.setEnabled(True)
        self.actionRelativeDate.setEnabled(True)
        self.populate_records()

    def populate_records(self, humanize=True):
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

        self.tableWidget.setRowCount(0)

        for row_num, key_name in enumerate(ord_recs):
            self.tableWidget.insertRow(row_num)
            for col_num, col_key in enumerate(ord_recs[key_name]):
                tbl_item = QTableWidgetItem(str(ord_recs[key_name][col_key]))
                self.tableWidget.setItem(row_num, col_num, tbl_item)

        self.welcome_lbl.setVisible(False)
        self.tableWidget.setVisible(False)
        self.tableWidget.verticalScrollBar().setValue(0)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setVisible(True)

    def show_student_page(self):
        name = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        nim = self.tableWidget.item(self.tableWidget.currentRow(), 1).text()
        self.student_glob = student_dir = name + "-" + nim
        self._student_ctrl = StudentController(self._model, self._controller,
                                               student_dir)
        self.log_tw.itemSelectionChanged.connect(self.selection_changed)
        self.display_logs(False)
        self.display_files()

        self.actionHide_SHA.setVisible(True)
        self.actionShow_SHA.setVisible(True)
        self.actionShow_stats.setVisible(True)
        self.actionHide_stats.setVisible(True)
        self.actionShow_Edit_distance.setVisible(True)

        self.actionShow_Edit_distance.triggered.connect(
            self.show_editdistance_view)
        self.actionShow_SHA.triggered.connect(lambda: self.toggle_sha(toogle=True))
        self.actionHide_SHA.triggered.connect(lambda: self.toggle_sha(toogle=False))
        self.actionShow_stats.triggered.connect(lambda: self.toogle_stats(toogle=True))
        self.actionHide_stats.triggered.connect(lambda: self.toogle_stats(toogle=False))

        self.stackedWidget.setCurrentIndex(1)

    def get_selected_sha(self):
        sha = 0
        items = self.log_tw.selectedItems()
        if items:
            sha = items[0].text(2)
        return sha

    def display_logs(self, complete=False):
        """Display log to log_QTreeWidget."""
        self.log_tw.hideColumn(2)  # hide SHA column (default)
        self.log_tw.hideColumn(3)
        self.log_tw.hideColumn(4)

        selected_file = self.get_selected_file()
        logs = self._student_ctrl.read_logs(selected_file)

        if complete:
            if selected_file:
                self.log_tw.clear()
                for l in logs:
                    QTreeWidgetItem(self.log_tw, [
                        str(l.relative_datetime),
                        str(l.datetime),
                        str(l.sha),
                        str(l.add_stats),
                        str(l.del_stats)
                    ])
                self.log_tw.showColumn(3)
                self.log_tw.showColumn(4)
                self.log_tw.resizeColumnToContents(3)
                self.log_tw.resizeColumnToContents(4)
            else:
                QMessageBox.warning(self, '', 'please choose a file')
        else:
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
        self.diff_pte.clear()
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
        self.file_tw.clear()
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
        if sha:
            self.display_diff(sha)
            self.display_windows(sha)
            self.display_auth_info(sha)

    def show_editdistance_view(self):
        selected_file = self.get_selected_file()
        if selected_file:
            editdistance_ax = self._student_ctrl.calc_editdistance_ax(
            selected_file)
            if editdistance_ax:
                self.editdistance_view = EditDistanceView(
                    editdistance_ax, self._student_ctrl, self.student_glob)
                self.editdistance_view.show()
        else:
            QMessageBox.warning(self, '', 'please choose a file')

    def toggle_sha(self, toogle=False):
        if toogle:
            self.log_tw.showColumn(2)
            self.log_tw.resizeColumnToContents(3)
        else:
            self.log_tw.hideColumn(2)
            self.log_tw.resizeColumnToContents(0)
            self.log_tw.resizeColumnToContents(1)
            self.log_tw.resizeColumnToContents(3)
            self.log_tw.resizeColumnToContents(4)

    def toogle_stats(self, toogle=False):
        if toogle:
            self.display_logs(True)
        else:
            self.log_tw.hideColumn(3)
            self.log_tw.hideColumn(4)
            self.log_tw.resizeColumnToContents(0)
            self.log_tw.resizeColumnToContents(1)
