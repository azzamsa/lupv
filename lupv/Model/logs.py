from PyQt5.QtCore import QObject


class Logs(QObject):
    def __init__(self, relative_datetime, datetime, sha):
        super().__init__()
        self.relative_datetime = relative_datetime
        self.datetime = datetime
        self.sha = sha
