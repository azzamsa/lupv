from Resources.theme import breeze_resources
from standard.standard import MyComboBox, bold, resize_column
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QTableWidgetItem,
    QApplication,
    QMessageBox,
    QTreeWidgetItem,
    QStyle,
    QLabel,
    QSizePolicy,
    qApp,
)

from PyQt5.QtCore import QFile, QTextStream, QSize, Qt
from PyQt5.QtGui import QKeySequence, QBrush, QColor, QIcon, QPixmap
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
        self._loaded_student_ed = None

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
            lambda: self.change_table_appearance("real")
        )
        self.main_reldate_rbtn.toggled.connect(
            lambda: self.change_table_appearance("rel")
        )

        #
        # Log view
        #

        ed_icon = "../lupv/Resources/img/chart-line.svg"
        self.show_editdistance_action.setIcon(QIcon(ed_icon))
        self.show_editdistance_action.setIconSize(QSize(16, 16))
        self.show_editdistance_action.clicked.connect(self.show_editdistance_view)

        self.log_tree.itemSelectionChanged.connect(self.log_selection_changed)

        self.stats_check.setToolTip("Show/hide insertions deletions lines")
        self.stats_check.clicked.connect(lambda: self.log_appearance_changed("stats"))

        self.sha_check.setToolTip("Show/hide SHA value")
        self.sha_check.clicked.connect(lambda: self.log_appearance_changed("sha"))

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

        #
        # Search View
        #
        self.analyze_suspects_btn.clicked.connect(self.display_suspects)

        self.suspect_filename_combo = MyComboBox()
        self.suspect_filename_combo.setEditable(True)
        self.suspect_filename_combo.setSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.Preferred
        )
        self.suspect_filename_combo.popupAboutToBeShown.connect(self.suggest_filename)
        self.horizontalLayout_5.addWidget(self.suspect_filename_combo)

        search_icon = "../lupv/Resources/img/account-search-outline.svg"
        self.analyze_suspects_btn.setIcon(QIcon(search_icon))
        self.analyze_suspects_btn.setIconSize(QSize(16, 16))
        self.analyze_suspects_btn.setToolTip(
            "Search for Suspect.\nThis might take a while"
        )

        self.windows_searchkey_widget.returnPressed.connect(self.display_window_search)
        self.windows_search_btn.clicked.connect(self.display_window_search)
        self.windows_search_btn.setIcon(QIcon(search_icon))
        self.windows_search_btn.setIconSize(QSize(16, 16))
        self.windows_search_btn.setToolTip(
            "Search window by name.\nThis might take a while"
        )

        self.group_by_ip_btn.clicked.connect(self.display_gropy_by_ip)
        self.group_by_ip_btn.setIcon(QIcon(search_icon))
        self.group_by_ip_btn.setIconSize(QSize(16, 16))
        self.group_by_ip_btn.setToolTip(
            "Group students by Ip Address.\nThis might take a while"
        )

        self.load_editdistance_action.triggered.connect(self.load_yaml)
        self.export_editdistance_action.triggered.connect(self.export_editdistance)
        self.compare_editdistance_btn.clicked.connect(
            self.display_compared_editdistance
        )

        # editdistance paged
        self.prev_student_name_combo = MyComboBox()
        self.prev_student_name_combo.setEditable(True)
        self.prev_student_name_combo.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Preferred
        )
        self.prev_student_name_combo.popupAboutToBeShown.connect(
            self.suggest_prev_editdistance_fields
        )
        self.horizontalLayout_18.addWidget(self.prev_student_name_combo)

        self.prev_filename_combo = MyComboBox()
        self.prev_filename_combo.setEditable(True)
        self.prev_filename_combo.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Preferred
        )
        self.prev_filename_combo.popupAboutToBeShown.connect(
            self.suggest_prev_editdistance_fields
        )
        self.horizontalLayout_19.addWidget(self.prev_filename_combo)

        self.cur_student_name_combo = MyComboBox()
        self.cur_student_name_combo.setEditable(True)
        self.cur_student_name_combo.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Preferred
        )
        self.cur_student_name_combo.popupAboutToBeShown.connect(
            self.suggest_cur_editdistance_fields
        )
        self.horizontalLayout_21.addWidget(self.cur_student_name_combo)

        self.cur_filename_combo = MyComboBox()
        self.cur_filename_combo.setEditable(True)
        self.cur_filename_combo.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Preferred
        )
        self.cur_filename_combo.popupAboutToBeShown.connect(
            self.suggest_cur_editdistance_fields
        )
        self.horizontalLayout_20.addWidget(self.cur_filename_combo)

        #  spinner
        hour_icon = "../lupv/Resources/img/hourglass.svg"
        hour_pixmap = QPixmap(hour_icon)
        self.spinner_lbl.setPixmap(hour_pixmap)

        # default
        self.stackedWidget.setVisible(False)
        self.widget.setVisible(False)
        self.spinner_stack.setCurrentIndex(0)
        self.welcome_lbl = QLabel()
        self.welcome_lbl.setText("Please open records to start analyzing")
        self.welcome_lbl.setStyleSheet("font-size: 20px;")
        self.welcome_lbl.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.welcome_lbl)
        self.horizontalLayout_2.addWidget(self.welcome_lbl)

        self.toggle_theme(light)
        self.stackedWidget.setCurrentIndex(0)
        self.show()

    def toggle_spinner(self, toggle):
        if toggle == "work":
            self.spinner_stack.setCurrentIndex(1)
        else:
            self.spinner_stack.setCurrentIndex(0)

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

    def choosefile_dialog(self, caption):
        """Prompts dialog to choose record directory."""
        # options = QFileDialog.ShowF | QFileDialog.DontResolveSymlinks
        return QFileDialog.getOpenFileName(self, caption=caption)

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

        self.toggle_spinner("work")
        qApp.processEvents()

        self._record_path = path
        self.display_records()
        self.toggle_spinner("ready")

    def display_records(self):
        """Populate records."""
        records = self._controller.read_records(self._record_path)

        self.main_table.setRowCount(0)

        for row_num, record in enumerate(records):
            self.main_table.insertRow(row_num)
            for col_num, record_item in enumerate(record.__dict__.items()):
                tbl_item = QTableWidgetItem(str(record_item[1]))
                self.main_table.setItem(row_num, col_num, tbl_item)

        self.main_table.setVisible(False)
        self.main_table.verticalScrollBar().setValue(0)
        self.main_table.resizeColumnsToContents()
        self.main_table.setVisible(True)

        self.change_table_appearance("rel")  # default
        self.main_reldate_rbtn.setChecked(True)
        self.main_realdate_rbtn.setChecked(False)

        self.welcome_lbl.setVisible(False)
        self.stackedWidget.setVisible(True)
        self.widget.setVisible(True)
        self.toogle_sidebar()

    def change_table_appearance(self, btn_name):
        if btn_name == "real":
            for col in range(3, 6):
                self.main_table.setColumnHidden(col, False)
            for col in range(6, 9):
                self.main_table.setColumnHidden(col, True)
        else:
            for col in range(3, 6):
                self.main_table.setColumnHidden(col, True)
            for col in range(6, 9):
                self.main_table.setColumnHidden(col, False)

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
        student_dir = self.get_selected_student()
        self._student_ctrl = StudentController(
            self._controller, self._record_path, student_dir
        )

        # default state
        for col in [0, 2, 3, 4]:
            self.log_tree.hideColumn(col)
        self.log_realdate_rbtn.setChecked(True)
        self.sha_check.setChecked(False)
        self.stats_check.setChecked(False)
        self.show_mode_rbtn.setChecked(True)

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
        self.toggle_spinner("work")
        qApp.processEvents()

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
                            else "{} Lines".format(l.del_stats)
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
        self.toggle_spinner("ready")

    def display_file_content(self, sha):
        """Display diff to diff_QPlainTextEdit."""
        self.file_content_widget.clear()

        if self.diff_mode_rbtn.isChecked():
            mode = "diff"
        else:
            mode = "show"

        selected_file = self.get_selected_file()
        no_file_selected_msg = "No file selected, Please select one"
        no_file_rec_msg = 'No availibale record for "{}" in this period'.format(
            selected_file
        )

        if not selected_file:
            self.file_content_widget.setPlainText(no_file_selected_msg)
        else:
            file_content = self._student_ctrl.read_file_content(
                selected_file, sha, mode
            )
            if file_content == "" or file_content is None:
                self.file_content_widget.setPlainText(no_file_rec_msg)
            else:
                if mode == "show":
                    self.file_content_widget.setPlainText(file_content)
                else:
                    self.file_content_widget.appendHtml(file_content)

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
            if window != focused_window:
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
                    self.stats_check.setChecked(False)
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
            self.toggle_spinner("work")
            qApp.processEvents()

            editdistance_ax = self._student_ctrl.calc_editdistance_ax(selected_file)
            if editdistance_ax:
                self.editdistance_view = EditDistanceView(
                    editdistance_ax, self._student_ctrl, student_dir
                )
                self.editdistance_view.show()

                self.toggle_spinner("ready")
        else:
            QMessageBox.warning(self, "", "Please choose a file")

    #
    # Search View
    #

    def suggest_filename(self):
        self.suspect_filename_combo.clear()

        student_sample = self._controller.get_student_sample(self._record_path)
        files = self._controller.get_sample_file(student_sample)
        files.insert(0, "No File Selected")
        self.suspect_filename_combo.addItems(files)

    def display_suspects(self):
        self.suspects_tree.clear()
        insertions_limit = str(self.insertions_limit_spin.value())
        filename = self.suspect_filename_combo.currentText()

        if int(insertions_limit) == 0:
            QMessageBox.warning(
                self,
                "",
                "please set limit higer than {}\nAbove 10 is recommended".format(
                    insertions_limit
                ),
            )
            return None
        if filename == "No File Selected" or not filename:
            QMessageBox.warning(self, "", "please select a file")
            return None

        self.toggle_spinner("work")
        qApp.processEvents()

        suspects = self._controller.get_suspects(
            self._record_path, int(insertions_limit), str(filename)
        )
        suspects_parentchild = self._controller.construct_parentchild(suspects)

        if len(suspects_parentchild.keys()) > 0:
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
        else:
            for col in range(1, 5):
                self.suspects_tree.hideColumn(col)
            self.suspects_tree.headerItem().setText(0, "")

            QTreeWidgetItem(
                self.suspects_tree,
                ['No suspect found, for "{}" insertion limit'.format(insertions_limit)],
            )
        resize_column(self.suspects_tree)
        self.toggle_spinner("ready")

    def display_gropy_by_ip(self):
        self.toggle_spinner("work")
        qApp.processEvents()

        self.group_by_ip_tree.clear()
        student_and_ip = self._controller.read_ips(self._record_path)
        ip_student_students = self._controller.group_by_ip(student_and_ip)

        if len(ip_student_students.keys()) > 0:
            for key in ip_student_students.keys():
                parent = QTreeWidgetItem(
                    self.group_by_ip_tree,
                    ["{} [{}]".format(key, len(ip_student_students[key]))],
                )
                bold(parent)
                for student in ip_student_students[key].keys():
                    child = QTreeWidgetItem(
                        parent,
                        [
                            "{} [{}]".format(
                                student, len(ip_student_students[key][student])
                            )
                        ],
                    )
                    for students in ip_student_students[key][student]:
                        QTreeWidgetItem(
                            child,
                            [
                                str(students.ip),
                                students.name,
                                str(students.nim),
                                students.date,
                            ],
                        )
        else:
            for col in range(1, 4):
                self.group_by_ip_tree.hideColumn(col)
            self.group_by_ip_tree.headerItem().setText(0, "")

            QTreeWidgetItem(self.group_by_ip_tree, ["No IP address found"])
        resize_column(self.group_by_ip_tree)
        self.toggle_spinner("ready")

    def display_window_search(self):
        self.toggle_spinner("work")
        qApp.processEvents()

        self.windows_search_tree.clear()
        search_key = self.windows_searchkey_widget.text()
        if not search_key:
            QMessageBox.warning(self, "", "please supply the window name")
            return None  # magic line `break` alias.

        student_windows = self._controller.read_windows(self._record_path, search_key)

        if student_windows:
            for student_window in student_windows:
                QTreeWidgetItem(
                    self.windows_search_tree,
                    [
                        student_window.window_name,
                        student_window.name,
                        str(student_window.nim),
                        student_window.date,
                    ],
                )
        else:
            for col in range(1, 5):
                self.windows_search_tree.hideColumn(col)
            self.windows_search_tree.headerItem().setText(0, "")

            QTreeWidgetItem(
                self.windows_search_tree,
                ['No windows name for "{}" found'.format(search_key)],
            )
        resize_column(self.windows_search_tree)
        self.toggle_spinner("ready")

    def export_editdistance(self):
        self.toggle_spinner("work")
        qApp.processEvents()

        self._controller.create_lupvnotes_dir(self._record_path)
        filename = self._controller.get_editdistance_path(
            self._record_path, "tugas-pkn"
        )
        students_ed = self._controller.read_editdistance(
            self._record_path, "tugas-pkn.md"
        )
        self._controller.export_editdistance(students_ed, filename)

        self.toggle_spinner("ready")

    def get_random_color(self):
        random_color = (
            random.uniform(0, 1),
            random.uniform(0, 1),
            random.uniform(0, 1),
        )
        return random_color

    def load_yaml(self):
        filename = self.choosefile_dialog("Select File")
        if not filename[0]:
            return None
        self._loaded_student_ed = self._controller.read_editdistance_file(filename[0])

    def suggest_prev_editdistance_fields(self):
        if self._loaded_student_ed:
            self.prev_student_name_combo.clear()
            # suggested_name.insert(0, "No Name Selected")
            prev_students = list(self._loaded_student_ed.keys())
            self.prev_student_name_combo.addItems(prev_students)
            student_sample = list(self._loaded_student_ed.keys())[0]
            suggested_filename = self._loaded_student_ed[student_sample]["task_name"]
            self.prev_filename_combo.clear()
            self.prev_filename_combo.addItem(suggested_filename)
        else:
            QMessageBox.warning(self, "", "Please load editdistance file first")

    def suggest_cur_editdistance_fields(self):
        student_sample = self._controller.get_student_sample(self._record_path)
        files = self._controller.get_sample_file(student_sample)
        files.insert(0, "No File Selected")
        cur_students = self._controller.get_student_dirs(self._record_path)
        self.cur_student_name_combo.clear()
        self.cur_student_name_combo.addItems(cur_students)
        self.cur_filename_combo.clear()
        self.cur_filename_combo.addItems(files)

    def display_compared_editdistance(self):
        if not all((
            self.prev_student_name_combo,
            self.prev_filename_combo,
            self.cur_student_name_combo,
            self.cur_filename_combo)
        ):
            QMessageBox.warning(self, "", "Please fill all the fields")
            return None

        prev_student_name = self.prev_student_name_combo.currentText()
        prev_filename = self.prev_filename_combo.currentText()
        cur_student_name = self.cur_student_name_combo.currentText()
        cur_filename = self.cur_filename_combo.currentText()

        prev_records_ax = self._loaded_student_ed[prev_student_name]["records_a"]
        prev_editdistance_ax = self._loaded_student_ed[prev_student_name][
            "editdistance_ax"
        ]
        cur_editdistance_ax = self._student_ctrl.calc_editdistance_ax(cur_filename)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.widget_2.setVisible(False)
        self.verticalLayout_22.addWidget(self.canvas)

        ax = self.figure.add_subplot(111)
        ax.plot(
            cur_editdistance_ax[1],
            cur_editdistance_ax[0],
            label=cur_student_name,
        )
        ax.plot(
            prev_editdistance_ax,
            prev_records_ax,
            label=prev_student_name,
        )
        ax.legend()

        plt.title("{} .. {}".format(cur_student_name, prev_student_name))
        plt.xlabel("Records count")
        plt.ylabel("Edit distance from final sumbission")

        self.canvas.draw()
