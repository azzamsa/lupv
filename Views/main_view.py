from Views.main_window import Ui_MainWindow

from collections import OrderedDict
from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QTableWidgetItem,
                             QApplication, QLabel)
from PyQt5.QtCore import QFile, QTextStream, Qt
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

        self.actionOpen_Task.triggered.connect(self.populate_records)
        self.actionQuit.triggered.connect(self.quit_app)
        self.actionQuit.setShortcut(QKeySequence("Ctrl+q"))

        # Toggle theme
        dark_theme = '../Lupv/Resources/theme/dark.qss'
        light_theme = '../Lupv/Resources/theme/light.qss'
        self.actionToggleDark.triggered.connect(
            lambda: self.toggle_theme(dark_theme))
        self.actionToggleLight.triggered.connect(
            lambda: self.toggle_theme(light_theme))
        self.toggle_theme('../Lupv/Resources/theme/dark.qss')  # default theme

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
        welcome_message = QLabel()
        welcome_message.setText("Please open tasks to start analyzing")
        welcome_message.setStyleSheet(css)
        self.verticalLayout.addWidget(welcome_message,
                                      alignment=Qt.AlignCenter)

        self.show()

    def toggle_theme(self, path):
        lupv = QApplication.instance()
        file = QFile(path)
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        lupv.setStyleSheet(stream.readAll())

    def choosedir_dialog(self, caption):
        """Prompts dialog to choose record directory"""
        options = (QFileDialog.ShowDirsOnly |
                   QFileDialog.DontResolveSymlinks)
        return QFileDialog.getExistingDirectory(self,
                                                caption=caption,
                                                options=options)

    def quit_app(self):
        QApplication.quit()

    def populate_records(self):
        path = self.choosedir_dialog('Select Directory...')
        if not path:
            return None

        records = self._main_controller.create_records(path)
        ordered_records = MyDict()

        for rec in records:
            ordered_records[rec.name]["name"] = rec.name
            ordered_records[rec.name]["nim"] = rec.nim
            ordered_records[rec.name]["record_amounts"] = rec.record_amounts
            ordered_records[rec.name]["work_duration"] = rec.work_duration
            ordered_records[rec.name]["first_record"] = rec.first_record
            ordered_records[rec.name]["last_record"] = rec.last_record

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
