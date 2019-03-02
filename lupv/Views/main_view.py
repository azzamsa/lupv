from Resources.theme import breeze_resources
from standard.standard import MyComboBox, bold, resize_column

from PyQt5.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QTableWidgetItem,
    QApplication,
    QMessageBox,
    QTreeWidgetItem,
    QStyle,
)

from PyQt5.QtCore import QFile, QTextStream, QSize
from PyQt5.QtGui import QKeySequence, QBrush, QColor, QIcon
from PyQt5.uic import loadUi

from standard import icons
from Controllers.student_controller import StudentController
from Views.editdistance_view import EditDistanceView


class MainView(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        main_window = "../lupv/Resources/ui/main_window.ui"
        loadUi(main_window, self)
        self._controller = controller
        self._record_path = ""
        self._records = None

        #
        # Sidebar
        #
        page1_icon = "../lupv/Resources/img/lup.svg"
        page2_icon = "../lupv/Resources/img/history-dim.svg"
        page3_icon = "../lupv/Resources/img/search-dim.svg"
        self.page1_btn.setIcon(QIcon(page1_icon))
        self.page1_btn.setIconSize(QSize(69, 69))
        self.page1_btn.setToolTip("Go to Main Window")

        self.page2_btn.setIcon(QIcon(page2_icon))
        self.page2_btn.setIconSize(QSize(64, 64))
        self.page2_btn.setToolTip("Go to Snapshot Window")
        self.page2_btn.setEnabled(False)

        self.page3_btn.setIcon(QIcon(page3_icon))
        self.page3_btn.setIconSize(QSize(64, 64))
        self.page3_btn.setToolTip("Go to Search Window")
        self.page3_btn.setEnabled(False)

        self.page1_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.page2_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.page3_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))

        #
        # MainView actions
        #
        open_icon = icons.style(QStyle.SP_DialogOpenButton)
        self.open_records_action.setIcon(open_icon)
        self.open_records_action.triggered.connect(self.open_records)
        self.open_records_action.setShortcut(QKeySequence("Ctrl+O"))
        self.quit_action.triggered.connect(self.quit_app)
        self.quit_action.setShortcut(QKeySequence("Ctrl+Q"))

        dark = "../lupv/Resources/theme/dark.qss"
        light = "../lupv/Resources/theme/light.qss"
        self.dark_theme_action.triggered.connect(lambda: self.toggle_theme(dark))
        self.light_theme_action.triggered.connect(lambda: self.toggle_theme(light))

        self.main_table.clicked.connect(self.show_student_view)
        self.main_table.setToolTip("Click me to analyze")

        self.main_realdate_rbtn.setToolTip("Use Real DateTime format")
        self.main_reldate_rbtn.setToolTip("Use Relative DateTime format")

        self.main_realdate_rbtn.toggled.connect(
            lambda: self.display_records(datetime_type=0)
        )
        self.main_reldate_rbtn.toggled.connect(
            lambda: self.display_records(datetime_type=1)
        )

        #
        # Search View
        #
        self.analyze_suspects_btn.clicked.connect(self.display_suspects)

        self.suspect_filename_combo = MyComboBox()
        self.suspect_filename_combo.setEditable(True)
        self.suspect_filename_combo.popupAboutToBeShown.connect(self.suggest_filename)
        self.verticalLayout_6.addWidget(self.suspect_filename_combo)

        search_icon = "../lupv/Resources/img/account-search-outline.svg"
        self.analyze_suspects_btn.setIcon(QIcon(search_icon))
        self.analyze_suspects_btn.setIconSize(QSize(24, 24))
        self.analyze_suspects_btn.setToolTip(
            "Search for Suspect.\nThis might take a while"
        )

        self.windows_search_btn.setIcon(QIcon(search_icon))
        self.windows_search_btn.setIconSize(QSize(16, 16))
        self.windows_search_btn.setToolTip(
            "Search window by name.\nThis might take a while"
        )

        self.group_by_ip_btn.setIcon(QIcon(search_icon))
        self.group_by_ip_btn.setIconSize(QSize(16, 16))
        self.group_by_ip_btn.setToolTip(
            "Group students by Ip Address.\nThis might take a while"
        )

        # default
        self.toggle_theme(light)
        self.stackedWidget.setCurrentIndex(0)
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

        self._record_path = path
        self.display_records()

    def display_records(self, datetime_type=1):
        """Populate records."""
        if self._records is None:
            self._records = self._controller.read_records(self._record_path)

        self.main_table.setRowCount(0)

        for row_num, record in enumerate(self._records):
            self.main_table.insertRow(row_num)
            for col_num, record_item in enumerate(record.__dict__.items()):
                if type(record_item[1]) is list:
                    item = record_item[1][datetime_type]
                else:
                    item = record_item[1]
                tbl_item = QTableWidgetItem(str(item))
                self.main_table.setItem(row_num, col_num, tbl_item)

        self.main_table.setVisible(False)
        self.main_table.verticalScrollBar().setValue(0)
        self.main_table.resizeColumnsToContents()
        self.main_table.setVisible(True)

        self.toogle_sidebar()

    def toogle_sidebar(self):
        page2_icon = "../lupv/Resources/img/history.svg"
        page3_icon = "../lupv/Resources/img/search.svg"
        self.page2_btn.setIcon(QIcon(page2_icon))
        self.page2_btn.setIconSize(QSize(64, 64))
        self.page2_btn.setEnabled(True)

        self.page3_btn.setIcon(QIcon(page3_icon))
        self.page3_btn.setIconSize(QSize(64, 64))
        self.page3_btn.setEnabled(True)

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
        record_path = self._record_path
        student_dir = self.get_selected_student()
        self._student_ctrl = StudentController(
            self._controller, record_path, student_dir
        )

        ed_icon = "../lupv/Resources/img/chart-line.svg"
        self.show_editdistance_action.setIcon(QIcon(ed_icon))
        self.show_editdistance_action.setIconSize(QSize(16, 16))
        self.show_editdistance_action.clicked.connect(self.show_editdistance_view)

        self.log_tree.itemSelectionChanged.connect(self.log_selection_changed)

        self.stats_check.setToolTip("Show/hide insertions deletions lines")
        self.stats_check.stateChanged.connect(
            lambda: self.log_appearance_changed("stats")
        )

        self.sha_check.setToolTip("Show/hide SHA value")
        self.sha_check.stateChanged.connect(lambda: self.log_appearance_changed("sha"))

        self.log_realdate_rbtn.setToolTip("Use Real DateTime format")
        self.log_realdate_rbtn.toggled.connect(
            lambda: self.log_appearance_changed("dateformat")
        )
        self.log_reldate_rbtn.setToolTip("Use Relative DateTime format")
        self.log_reldate_rbtn.toggled.connect(
            lambda: self.log_appearance_changed("dateformat")
        )

        self.diff_mode_rbtn.setToolTip("Use diff mode for file contents")
        self.show_mode_rbtn.setToolTip("Use show mode for file contents")
        self.filename_combo.setToolTip("Filename to track")

        # default state
        self.log_tree.hideColumn(1)
        self.log_tree.hideColumn(2)
        self.log_tree.hideColumn(3)
        self.log_tree.hideColumn(4)

        # init functions
        self.clear_widgets()
        self.display_logs(False)
        self.supply_filename()
        self.stackedWidget.setCurrentIndex(1)

    def clear_widgets(self):
        """Clear all widget contents."""
        self.file_content_widget.clear()
        self.log_tree.clear()
        self.filename_combo.clear()
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

        selected_file = self.get_selected_file()
        logs = self._student_ctrl.read_logs(selected_file)

        if complete:  # can't show stats without selected_file
            self.log_tree.clear()
            for l in logs:
                QTreeWidgetItem(
                    self.log_tree,
                    [
                        str(l.relative_datetime),
                        str(l.datetime),
                        str(l.sha),
                        "{line}".format(
                            line="No record"
                            if l.add_stats == 0
                            else "{} Lines".format(l.add_stats)
                        ),
                        "{line}".format(
                            line="No record"
                            if l.del_stats == 0
                            else "{} Lines".format(l.add_stats)
                        ),
                    ],
                )
        else:
            for l in logs:
                QTreeWidgetItem(
                    self.log_tree,
                    [str(l.relative_datetime), str(l.datetime), str(l.sha)],
                )

        resize_column(self.log_tree)

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

    def supply_filename(self):
        """Display file to file_QTreeWidget."""
        # self.filename_combo.clear()
        student_dir = self._student_ctrl.get_student_path()
        files = self._controller.get_files(student_dir)
        files.insert(0, "No File Selected")
        self.filename_combo.addItems(files)

    def get_selected_file(self):
        """Return selected file in file_QTreeWidget."""
        filename = str(self.filename_combo.currentText())
        if filename != "No File Selected":
            return filename

    def display_windows(self, sha):
        """Display all windows and focused window from self.records."""
        self.windows_tree.clear()

        focused_window = self._student_ctrl.read_focused_window(sha)
        focused_row = QTreeWidgetItem(self.windows_tree, [focused_window])

        focused_row.setForeground(0, QBrush(QColor("#41CD52")))
        windows = self._student_ctrl.read_all_windows(sha)
        for window in windows:
            if windoself.w != focused_window:
                QTreeWidgetItem(self.windows_tree, [window])

    def display_auth_info(self, sha):
        """Display auth information from self.records."""
        auth_info = self._student_ctrl.read_auth_info(sha)
        if auth_info:
            self.name_lbl.setText(auth_info[0])
            self.machine_lbl.setText(auth_info[1])
            self.ip_lbl.setText(auth_info[2])

    def log_selection_changed(self):
        """Actions invoked when selection in log_QTreeWidget changed."""
        sha = self.get_selected_sha()
        if sha:
            self.display_file_content(sha)
            self.display_windows(sha)
            self.display_auth_info(sha)

    def log_appearance_changed(self, btn_name):
        if btn_name == "stats":
            if self.stats_check.isChecked():
                selected_file = self.get_selected_file()
                if selected_file:
                    self.display_logs(True)
                    self.log_tree.showColumn(3)
                    self.log_tree.showColumn(4)
                else:
                    QMessageBox.warning(self, "", "please choose a file")
            else:
                self.log_tree.hideColumn(3)
                self.log_tree.hideColumn(4)
        elif btn_name == "sha":
            if self.sha_check.isChecked():
                self.log_tree.showColumn(2)
            else:
                self.log_tree.hideColumn(2)
        elif btn_name == "dateformat":
            if self.log_realdate_rbtn.isChecked():
                self.log_tree.hideColumn(0)
                self.log_tree.showColumn(1)
            else:
                self.log_tree.hideColumn(1)
                self.log_tree.showColumn(0)
        resize_column(self.log_tree)

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

    #
    # Search View
    #

    def suggest_filename(self):
        student_sample = self._controller.get_student_sample(self._record_path)
        files = self._controller.get_sample_file(student_sample)
        self.suspect_filename_combo.clear()
        self.suspect_filename_combo.addItems(files)

    def display_suspects(self):
        self.suspects_tree.clear()
        insertions_limit = str(self.insertions_limit_spin.value())
        filename = "tugas-pkn.md"
        suspects = self._controller.get_suspects(
            self._record_path, int(insertions_limit), str(filename)
        )
        suspects_parentchild = self._controller.construct_parentchild(suspects)

        # track parents column
        parents = {}
        for key in suspects_parentchild.keys():
            parent = QTreeWidgetItem(
                self.suspects_tree,
                ["{} [{}]".format(key, len(suspects_parentchild[key]))],
            )
            bold(parent)
            for suspect in suspects_parentchild[key]:
                QTreeWidgetItem(
                    parent,
                    [
                        suspect.name,
                        str(suspect.nim),
                        suspect.filename,
                        str(suspect.insertions),
                        str(suspect.date),
                    ],
                )
        resize_column(self.suspects_tree)
