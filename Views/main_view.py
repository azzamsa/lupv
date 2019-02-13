from Views.main_window import Ui_MainWindow

from collections import OrderedDict
from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QTableWidgetItem,
                             QApplication)
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QKeySequence


class MyDict(OrderedDict):
    def __missing__(self, key):
        val = self[key] = MyDict()
        return val


class MainView(QMainWindow, Ui_MainWindow):

    def __init__(self, model, main_controller):
        super().__init__()
        self._model = model
        self._main_controller = main_controller
        self.setupUi(self)
        self.show()

        self.actionOpen_Task.triggered.connect(self.load_data)
        self.actionQuit.triggered.connect(self.quit_app)
        self.actionQuit.setShortcut(QKeySequence("Ctrl+q"))

        # Toggle theme
        dark_theme = '../Lupv/Resources/theme/dark.qss'
        light_theme = '../Lupv/Resources/theme/light.qss'
        self.actionToggleDark.triggered.connect(lambda: self.toggle_theme(dark_theme))
        self.actionToggleLight.triggered.connect(lambda: self.toggle_theme(light_theme))
        self.toggle_theme('../Lupv/Resources/theme/dark.qss')  # default theme

    def toggle_theme(self, path):
        lupv = QApplication.instance()
        file = QFile(path)
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        lupv.setStyleSheet(stream.readAll())

    def choose_record_dir(self):
        record_dir = str(QFileDialog.getExistingDirectory(self,
                                                          "Select Directory"))
        self._main_controller.set_record_dir(record_dir)

    def read_tasks(self):
        self.choose_record_dir()
        self._main_controller.create()

    def quit_app(self):
        QApplication.quit()

    def load_data(self):
        self.choose_record_dir()
        records = self._main_controller.create_records()
        ordered_records = MyDict()

        for record in records:
            ordered_records[record.name]["name"] = record.name
            ordered_records[record.name]["nim"] = record.nim
            ordered_records[record.name]["record_amounts"] = record.record_amounts
            ordered_records[record.name]["work_duration"] = record.work_duration
            ordered_records[record.name]["first_record"] = record.first_record
            ordered_records[record.name]["last_record"] = record.last_record

        self.tableWidget.setRowCount(0)

        for row_number, key_name in enumerate(ordered_records):
            self.tableWidget.insertRow(row_number)
            for column_number, column_key in enumerate(
                    ordered_records[key_name]):
                table_item = QTableWidgetItem(
                    str(ordered_records[key_name][column_key]))
                self.tableWidget.setItem(row_number, column_number,
                                         table_item)
        self.tableWidget.setVisible(False)
        self.tableWidget.verticalScrollBar().setValue(0)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setVisible(True)
