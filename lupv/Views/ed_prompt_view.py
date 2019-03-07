from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class EditdistancePrompt(QDialog):
    def __init__(self):
        super().__init__()
        ed_prompt = "../lupv/Resources/ui/ed_prompt.ui"
        loadUi(ed_prompt, self)

        self.cancel_btn.clicked.connect(self.close)
        self.export_btn.clicked.connect(self.accept)
