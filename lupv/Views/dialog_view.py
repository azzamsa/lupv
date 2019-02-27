from PyQt5.QtWidgets import QDialog
from Views.suspect import Ui_Dialog


class SuspectDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.cancel_action.clicked.connect(self.close)
        self.analyze_action.clicked.connect(self.accept)
