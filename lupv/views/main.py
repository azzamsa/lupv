from resources.theme import breeze_resources

from PyQt5.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QTableWidgetItem,
    QApplication,
    QMessageBox,
    QStyle,
    QLabel,
    qApp,
)

from PyQt5.QtCore import QFile, QTextStream, QSize, Qt, pyqtSlot
from PyQt5.QtGui import QKeySequence, QIcon, QPixmap

from resources import resources
from standard.standard import icon_style
from models.logs import LogModel
from models.search import SearchModel
from controllers.log import LogController
from controllers.search import SearchController
from views.main_ui import Ui_MainWindow
from views.log import LogView
from views.search import SearchView


class MainView(QMainWindow):
    def __init__(self, main_ctrl, main_model):
        super().__init__()
        self._main_ctrl = main_ctrl
        self._main_model = main_model
        self._record_path = ""
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        # Other page object
        self._log_model = LogModel(self._main_model)
        self._log_ctrl = LogController(self._main_ctrl, self._log_model)

        self._search_model = SearchModel(self._main_model)
        self._search_ctrl = SearchController(
            self._main_model, self._search_model, self._log_model
        )
        self._search_view = SearchView(self._ui, self._search_ctrl)

        # Observers
        self._main_model.record_path_changed.connect(self.on_record_path_changed)

        # Sidebar
        self._ui.page1_btn.setIcon(QIcon(":img/lup.svg"))
        self._ui.page1_btn.setIconSize(QSize(69, 69))
        self._ui.page1_btn.setToolTip("Go to Main Window")

        self._ui.page2_btn.setIcon(QIcon(":img/history-dim.svg"))
        self._ui.page2_btn.setIconSize(QSize(64, 64))
        self._ui.page2_btn.setToolTip("Go to Snapshot Window")
        self._ui.page2_btn.setEnabled(False)

        self._ui.page3_btn.setIcon(QIcon(":img/search-dim.svg"))
        self._ui.page3_btn.setIconSize(QSize(64, 64))
        self._ui.page3_btn.setToolTip("Go to Search Window")
        self._ui.page3_btn.setEnabled(False)

        self._ui.page1_btn.clicked.connect(
            lambda: self._ui.stackedWidget.setCurrentIndex(0)
        )
        self._ui.page2_btn.clicked.connect(
            lambda: self._ui.stackedWidget.setCurrentIndex(1)
        )
        self._ui.page3_btn.clicked.connect(self.show_search_view)

        # Main View actions
        open_icon = icon_style(QStyle.SP_DialogOpenButton)
        self._ui.open_records_action.setIcon(open_icon)
        self._ui.open_records_action.triggered.connect(self.open_records)
        self._ui.open_records_action.setShortcut(QKeySequence("Ctrl+O"))
        self._ui.quit_action.triggered.connect(self.quit_app)
        self._ui.quit_action.setShortcut(QKeySequence("Ctrl+Q"))

        dark = ":theme/dark.qss"
        light = ":theme/light.qss"
        self._ui.dark_theme_action.triggered.connect(lambda: self.toggle_theme(dark))
        self._ui.light_theme_action.triggered.connect(lambda: self.toggle_theme(light))

        self._ui.main_table.clicked.connect(self.show_log_view)
        self._ui.main_table.setToolTip("Click me to analyze")

        self._ui.main_realdate_rbtn.setToolTip("Use Real DateTime format")
        self._ui.main_reldate_rbtn.setToolTip("Use Relative DateTime format")

        self._ui.main_realdate_rbtn.toggled.connect(
            lambda: self.change_table_appearance("real")
        )
        self._ui.main_reldate_rbtn.toggled.connect(
            lambda: self.change_table_appearance("rel")
        )

        hour_pixmap = QPixmap(":img/hourglass.svg")
        self._ui.spinner_lbl.setPixmap(hour_pixmap)

        self.welcome_lbl = QLabel()
        self.welcome_lbl.setText("Please open records to start analyzing")
        self.welcome_lbl.setStyleSheet("font-size: 20px;")
        self.welcome_lbl.setAlignment(Qt.AlignCenter)
        self._ui.verticalLayout.addWidget(self.welcome_lbl)
        self._ui.horizontalLayout_2.addWidget(self.welcome_lbl)

        # default
        self._ui.stackedWidget.setVisible(False)
        self._ui.widget.setVisible(False)
        self._ui.spinner_stack.setCurrentIndex(0)
        self._ui.load_editdistance_action.setEnabled(False)
        self._ui.export_editdistance_action.setEnabled(False)
        self._ui.tabWidget.tabBar().setExpanding(True)
        self.toggle_theme(light)
        self._ui.stackedWidget.setCurrentIndex(0)

    def toggle_spinner(self, toggle):
        if toggle == "work":
            self._ui.spinner_stack.setCurrentIndex(1)
        else:
            self._ui.spinner_stack.setCurrentIndex(0)

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

    def is_valid(self, path):
        """Check if path is record path."""
        invalid_dirs = self._main_ctrl.validate(path)

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
            if not self.is_valid(path):
                return None

        self.toggle_spinner("work")
        qApp.processEvents()

        self._main_ctrl.change_record_path(path)
        self.display_records()

        self.toggle_spinner("ready")

    def display_records(self):
        """Populate records."""
        self._ui.main_table.setRowCount(0)

        for row_num, record in enumerate(self._main_ctrl.populate_students_records()):
            self._ui.main_table.insertRow(row_num)
            for col_num, record_item in enumerate(record.__dict__.items()):
                tbl_item = QTableWidgetItem(str(record_item[1]))
                self._ui.main_table.setItem(row_num, col_num, tbl_item)

        self._ui.main_table.setVisible(False)
        self._ui.main_table.verticalScrollBar().setValue(0)
        self._ui.main_table.resizeColumnsToContents()
        self._ui.main_table.setVisible(True)

        self.change_table_appearance("rel")  # default
        self._ui.main_reldate_rbtn.setChecked(True)
        self._ui.main_realdate_rbtn.setChecked(False)

        self.toggle_main_widgets()
        self.toogle_sidebar()

    def change_table_appearance(self, btn_name):
        rel_col_hidden = True
        real_col_hidden = False
        rel_col_nums = [4, 6, 8]
        real_col_nums = [3, 5, 7]

        if btn_name == "rel":
            rel_col_hidden = False
            real_col_hidden = True

        for real_col, rel_col in zip(rel_col_nums, real_col_nums):
            self._ui.main_table.setColumnHidden(real_col, real_col_hidden)
            self._ui.main_table.setColumnHidden(rel_col, rel_col_hidden)

    def toggle_main_widgets(self):
        self.welcome_lbl.setVisible(False)
        self._ui.stackedWidget.setVisible(True)
        self._ui.widget.setVisible(True)
        self._ui.load_editdistance_action.setEnabled(True)
        self._ui.export_editdistance_action.setEnabled(True)

    def toogle_sidebar(self):
        self._ui.page2_btn.setIcon(QIcon(":img/history.svg"))
        self._ui.page2_btn.setIconSize(QSize(64, 64))
        self._ui.page2_btn.setEnabled(True)

        self._ui.page3_btn.setIcon(QIcon(":img/search.svg"))
        self._ui.page3_btn.setIconSize(QSize(64, 64))
        self._ui.page3_btn.setEnabled(True)

    @pyqtSlot(str)
    def on_record_path_changed(self, path):
        self._log_ctrl.change_record_path(path)

    def get_selected_student(self):
        """Return selected student from main table"""
        name = self._ui.main_table.item(self._ui.main_table.currentRow(), 0).text()
        student_id = self._ui.main_table.item(
            self._ui.main_table.currentRow(), 1
        ).text()
        current_student = "{}-{}".format(name, student_id)
        return current_student

    def show_log_view(self):
        """Show Student Page and do initial things."""
        current_student = self.get_selected_student()
        self._log_ctrl.change_current_student(current_student)
        self._log_view = LogView(self._ui, self._log_ctrl, self._main_ctrl)

    def show_search_view(self):
        self._ui.stackedWidget.setCurrentIndex(2)
