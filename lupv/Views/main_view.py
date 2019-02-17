import os
from Resources.theme import breeze_resources
from Views.main_window import Ui_MainWindow
from Views.student_view import StudentView

from collections import OrderedDict
from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QTableWidgetItem,
                             QApplication, QLabel, QMessageBox)
from PyQt5.QtCore import QFile, QTextStream, Qt
from PyQt5.QtGui import QKeySequence


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

        self.actionOpen_Records.triggered.connect(self.populate_records)
        self.actionOpen_Records.setShortcut(QKeySequence("Ctrl+O"))
        self.actionQuit.triggered.connect(self.quit_app)
        self.actionQuit.setShortcut(QKeySequence("Ctrl+Q"))
        self.tableWidget.clicked.connect(self.show_student_view)

        # Toggle theme
        dark = '../lupv/Resources/theme/dark.qss'
        light = '../lupv/Resources/theme/light.qss'
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

        self.tableWidget.setVisible(False)
        self.welcome_lbl = QLabel()
        self.welcome_lbl.setText("Please open records to start analyzing")
        self.welcome_lbl.setStyleSheet(css)
        self.verticalLayout.addWidget(self.welcome_lbl,
                                      alignment=Qt.AlignCenter)

        self.show()

    def quit_app(self):
        """Quit application"""
        QApplication.quit()
        self.close()

    def toggle_theme(self, path):
        """Change application theme based on theme location"""
        lupv = QApplication.instance()
        file = QFile(path)
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        lupv.setStyleSheet(stream.readAll())

    def choosedir_dialog(self, caption):
        """Prompts dialog to choose record directory"""
        options = (QFileDialog.ShowDirsOnly |
                   QFileDialog.DontResolveSymlinks)
        return QFileDialog.getExistingDirectory(self, caption=caption,
                                                options=options)

    def validate_path(self, path):
        """Validate chosen path.

        This is necessary because invalid path will break `read_records` and
        make application crash.
        """
        dirs = os.listdir(path)
        invalid_dirs = []
        for d in dirs:
            if not os.path.isdir(path + '/' + d + "/.git"):
                invalid_dirs.append(d)
        if len(invalid_dirs) == 0:
            return True
        elif len(invalid_dirs) <= 10:
            QMessageBox.warning(self, '', 'Not a valid Tasks directory'
                                '\n\nContains invalid Task: \n'
                                + '\n'.join(invalid_dirs))
        else:
            QMessageBox.warning(self, '', 'Not a valid Tasks directory'
                                '\n\nContains many invalid Tasks ')

    def save_record_path(self, record_path):
        "save record path"
        self._controller.save_record_path(record_path)

    def populate_records(self):
        "Populate record to Table"
        path = self.choosedir_dialog('Select Directory...')
        if not path:
            return None
        else:
            if not self.validate_path(path):
                return None

        self.save_record_path(path)
        humanize = True
        recs = self._controller.read_records(path, humanize)
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

    def show_student_view(self):
        """Show student view when tableWidget clicked"""
        name = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        nim = self.tableWidget.item(self.tableWidget.currentRow(), 1).text()
        student_dir = name + "-" + nim
        self.student_view = StudentView(self._model,
                                        self._controller, student_dir)
        self.student_view.show()
