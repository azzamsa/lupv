from PyQt5.QtCore import QObject


class Logs(QObject):
    def __init__(self, name, summary, email, sha):
        super().__init__()
        self.name = name
        self.summary = summary
        self.email = email
        self.sha = sha
