from PyQt5.QtWidgets import QDialog, QStyle
from Views.suspect_dialog import Ui_Dialog
from Views import icons


class SuspectDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        close_icon = icons.style(QStyle.SP_DialogCancelButton)
        ok_icon = icons.style(QStyle.SP_DialogOkButton)

        self.cancel_action.setIcon(close_icon)
        self.cancel_action.clicked.connect(self.close)
        self.analyze_action.setIcon(ok_icon)
        self.analyze_action.clicked.connect(self.accept)
