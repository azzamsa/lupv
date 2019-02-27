from Resources.theme import breeze_resources
from Views.standard import MyDict

from PyQt5.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QTableWidgetItem,
    QApplication,
    QLabel,
    QMessageBox,
    QTreeWidgetItem,
    QStyle,
)
from PyQt5.QtCore import QFile, QTextStream, Qt
from PyQt5.QtGui import QKeySequence, QBrush, QColor

from Views import icons
from Views.main_window import Ui_MainWindow
from Views.dialog_view import SuspectDialog
from Controllers.student_controller import StudentController
from Views.editdistance_view import EditDistanceView


class MainView(QMainWindow, Ui_MainWindow):
    def __init__(self, controller):
        super().__init__()
        self._controller = controller
        self.setupUi(self)

        # mainview actions
        open_icon = icons.style(QStyle.SP_DialogOpenButton)
        self.open_records_action.setIcon(open_icon)
        self.open_records_action.triggered.connect(self.open_records)
        self.open_records_action.setShortcut(QKeySequence("Ctrl+O"))
        self.quit_action.triggered.connect(self.quit_app)
        self.quit_action.setShortcut(QKeySequence("Ctrl+Q"))

        self.main_table.clicked.connect(self.show_student_view)
        self.main_table.setToolTip("Click me to analyze")
        self.toggle_realdate_action.triggered.connect(
            lambda: self.display_records(self.record_path, humanize=False)
        )
        self.toggle_relativedate_action.triggered.connect(
            lambda: self.display_records(self.record_path, humanize=True)
        )
        self.toggle_realdate_action.setEnabled(False)  # default
        self.toggle_relativedate_action.setEnabled(False)

        self.stackedWidget.setCurrentIndex(0)
        self.enable_actions_menu(page=0)

        self.analyze_suspect_action.triggered.connect(self.prompt_suspect_dialog)
        self.to_mainview_btn2.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(0)
        )
        # Toggle theme
        dark = "../lupv/Resources/theme/dark.qss"
        light = "../lupv/Resources/theme/light.qss"
        self.toogle_dark_action.triggered.connect(lambda: self.toggle_theme(dark))
        self.toogle_light_action.triggered.connect(lambda: self.toggle_theme(light))
        self.toggle_theme(light)  # default theme

        css = """
        color: white;
        font-size: 12px;
        border-radius: 12px;
        qproperty-alignment: AlignCenter;
        min-height: 25px;
        min-width: 250px;
        background: #1d2c3a;
        """

        self.main_table.setVisible(False)
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

    def choosepath_dialog(self, caption):
        """Prompts dialog to choose record directory."""
        options = QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        return QFileDialog.getExistingDirectory(self, caption=caption, options=options)

    def is_valid_path(self, path):
        """Check validity of given path."""
        invalid_dirs = self._controller.validate_path(path)

        msg = "Not a valid Tasks directory\n"
        details = "\nContains invalid Task:\n{}".format("\n".join(invalid_dirs))

        if len(invalid_dirs) == 0:
            return True
        elif len(invalid_dirs) <= 10:
            QMessageBox.warning(self, "", msg + details)
        else:
            QMessageBox.warning(self, "", msg + "\n\nContains many invalid Tasks")

    def open_records(self):
        """Open records directory then display the record."""
        path = self.choosepath_dialog("Select Directory...")
        if not path:
            return None
        else:
            if not self.is_valid_path(path):
                return None

        self.record_path = path
        self.display_records(path)

        self.toggle_realdate_action.setEnabled(True)
        self.toggle_relativedate_action.setEnabled(True)

    def display_records(self, path, humanize=True):
        """Populate records."""
        records = self._controller.read_records(path, humanize)
        ord_records = MyDict()  # ordered records

        for record in records:
            ord_records[record.name]["name"] = record.name
            ord_records[record.name]["nim"] = record.nim
            ord_records[record.name]["record_amounts"] = record.record_amounts
            ord_records[record.name]["work_duration"] = record.work_duration
            ord_records[record.name]["first_record"] = record.first_record
            ord_records[record.name]["last_record"] = record.last_record

        self.main_table.setRowCount(0)

        for row_num, key_name in enumerate(ord_records):
            self.main_table.insertRow(row_num)
            for col_num, col_key in enumerate(ord_records[key_name]):
                tbl_item = QTableWidgetItem(str(ord_records[key_name][col_key]))
                self.main_table.setItem(row_num, col_num, tbl_item)

        self.welcome_lbl.setVisible(False)

        self.main_table.setVisible(False)
        self.main_table.verticalScrollBar().setValue(0)
        self.main_table.resizeColumnsToContents()
        self.main_table.setVisible(True)

    def prompt_suspect_dialog(self):
        """Prompt dialog for suspect parameter."""
        suspect_dlg = SuspectDialog()
        accepted = suspect_dlg.exec_()
        if accepted:
            filename = suspect_dlg.filename_widget.text()
            insertions_limit = suspect_dlg.insertion_limit_widget.text()
            if insertions_limit and filename:
                self.display_suspects(insertions_limit, filename)
            else:
                QMessageBox.warning(self, "", "Please supply a value")
                self.prompt_suspect_dialog()

    def display_suspects(self, insertions_limit, filename):
        """Display suspect result."""
        suspects = self._controller.get_suspect(
            self.record_path, int(insertions_limit), str(filename)
        )
        ordered_suspects = MyDict()

        for suspect in suspects:
            ordered_suspects[suspect.name]["name"] = suspect.name
            ordered_suspects[suspect.name]["nim"] = suspect.nim
            ordered_suspects[suspect.name]["filename"] = suspect.filename
            ordered_suspects[suspect.name]["insertions"] = suspect.insertions
            ordered_suspects[suspect.name]["date"] = suspect.date

        for row_num, key_name in enumerate(ordered_suspects):
            self.suspect_table.insertRow(row_num)
            for col_num, col_key in enumerate(ordered_suspects[key_name]):
                tbl_item = QTableWidgetItem(str(ordered_suspects[key_name][col_key]))
                self.suspect_table.setItem(row_num, col_num, tbl_item)

        self.suspect_table.setVisible(False)
        self.suspect_table.verticalScrollBar().setValue(0)
        self.suspect_table.resizeColumnsToContents()
        self.suspect_table.setVisible(True)
        self.stackedWidget.setCurrentIndex(2)

    def get_selected_student(self):
        """Return selected student from main table"""
        name = self.main_table.item(self.main_table.currentRow(), 0).text()
        nim = self.main_table.item(self.main_table.currentRow(), 1).text()
        student_dir = name + "-" + nim
        return student_dir

    #
    # Student View
    #

    def show_student_view(self):
        """Show Student Page and do initial things."""
        # named column for easier reading
        self.reldate_col = 0
        self.datetime_col = 1
        self.sha_col = 2
        self.insertions_col = 3
        self.deletions_col = 4

        self.to_mainview_btn.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(0)
        )
        self.show_editdistance_action.triggered.connect(self.show_editdistance_view)
        self.show_sha_action.triggered.connect(lambda: self.toggle_sha(toogle=True))
        self.hide_sha_action.triggered.connect(lambda: self.toggle_sha(toogle=False))
        self.show_stats_action.triggered.connect(lambda: self.toogle_stats(toogle=True))
        self.hide_stats_action.triggered.connect(
            lambda: self.toogle_stats(toogle=False)
        )

        record_path = self.record_path
        student_dir = self.get_selected_student()
        self._student_ctrl = StudentController(
            self._controller, record_path, student_dir
        )

        self.log_tree.itemSelectionChanged.connect(self.selection_changed)
        self.clear_widgets()
        self.enable_actions_menu(page=1)

        self.display_logs(False)
        self.display_files()
        self.stackedWidget.setCurrentIndex(1)

    def enable_actions_menu(self, page):
        if page == 0:
            # main page actions
            self.toggle_realdate_action.setEnabled(True)
            self.toggle_relativedate_action.setEnabled(True)

            # student page actions
            self.hide_sha_action.setEnabled(False)
            self.show_sha_action.setEnabled(False)
            self.show_stats_action.setEnabled(False)
            self.hide_stats_action.setEnabled(False)
            self.show_editdistance_action.setEnabled(False)
        elif page == 1:
            # main page actions
            self.toggle_realdate_action.setEnabled(False)
            self.toggle_relativedate_action.setEnabled(False)

            # student page actions
            self.hide_sha_action.setEnabled(True)
            self.show_sha_action.setEnabled(True)
            self.show_stats_action.setEnabled(True)
            self.hide_stats_action.setEnabled(True)
            self.show_editdistance_action.setEnabled(True)

    def clear_widgets(self):
        """Clear all widget contents."""
        self.file_content_widget.clear()
        self.log_tree.clear()
        self.file_tree.clear()
        self.windows_tree.clear()

    def get_selected_sha(self):
        """Get SHA value from log_QTreeWidget."""
        sha = 0
        items = self.log_tree.selectedItems()
        if items:
            sha = items[0].text(2)
        return sha

    def display_logs(self, complete=False):
        """Display log to log_QTreeWidget."""
        self.log_tree.clear()

        self.log_tree.hideColumn(self.sha_col)
        self.log_tree.hideColumn(self.insertions_col)
        self.log_tree.hideColumn(self.deletions_col)

        selected_file = self.get_selected_file()
        logs = self._student_ctrl.read_logs(selected_file)

        if complete:
            if selected_file:
                self.log_tree.clear()
                for l in logs:
                    QTreeWidgetItem(
                        self.log_tree,
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
                self.log_tree.showColumn(self.insertions_col)
                self.log_tree.showColumn(self.deletions_col)
                self.log_tree.resizeColumnToContents(self.insertions_col)
                self.log_tree.resizeColumnToContents(self.deletions_col)
            else:
                QMessageBox.warning(self, "", "please choose a file")
        else:
            for l in logs:
                QTreeWidgetItem(
                    self.log_tree,
                    [str(l.relative_datetime), str(l.datetime), str(l.sha)],
                )

        self.log_tree.resizeColumnToContents(0)
        self.log_tree.resizeColumnToContents(1)

    def display_file_content(self, sha):
        """Display diff to diff_QPlainTextEdit."""
        self.file_content_widget.clear()

        selected_file = self.get_selected_file()
        no_file_selected_msg = "No file selected, Please select one"
        no_file_rec_msg = "No availibale record for {} in this period".format(
            selected_file
        )

        if not selected_file:
            self.file_content_widget.setPlainText(no_file_selected_msg)
        else:
            file_content = self._student_ctrl.read_file_content(selected_file, sha)
            if file_content == "":
                self.file_content_widget.setPlainText(no_file_rec_msg)
            else:
                self.file_content_widget.setPlainText(file_content)

    def display_files(self):
        """Display file to file_QTreeWidget."""
        self.file_tree.clear()
        student_dir = self._student_ctrl.get_student_path()
        files = self._controller.get_files(student_dir)
        for f in files:
            QTreeWidgetItem(self.file_tree, [f])

    def get_selected_file(self):
        """Return selected file in file_QTreeWidget."""
        items = self.file_tree.selectedItems()
        if items:
            selected_file = items[0].text(0)
            return selected_file

    def display_windows(self, sha):
        """Display all windows and focused window from records."""
        self.windows_tree.clear()

        focused_window = self._student_ctrl.read_focused_window(sha)
        focused_row = QTreeWidgetItem(self.windows_tree, [focused_window])

        focused_row.setForeground(0, QBrush(QColor("#41CD52")))
        windows = self._student_ctrl.read_all_windows(sha)
        for window in windows:
            if window != focused_window:
                QTreeWidgetItem(self.windows_tree, [window])

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
            self.display_file_content(sha)
            self.display_windows(sha)
            self.display_auth_info(sha)

    def toggle_sha(self, toogle=False):
        """Toggle the appearance of SHA columns."""
        if toogle:
            self.log_tree.showColumn(self.sha_col)
        else:
            self.log_tree.hideColumn(self.sha_col)
        for col in range(5):
            if col != 2:
                self.log_tree.resizeColumnToContents(col)

    def toogle_stats(self, toogle=False):
        """Toggle the appearance of stats columns."""
        if toogle:
            self.display_logs(True)
        else:
            self.log_tree.hideColumn(self.insertions_col)
            self.log_tree.hideColumn(self.deletions_col)
            self.log_tree.resizeColumnToContents(self.datetime_col)
            self.log_tree.resizeColumnToContents(self.sha_col)

    #
    # EditDistance View
    #

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
