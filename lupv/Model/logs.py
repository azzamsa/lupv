from PyQt5.QtCore import QObject


class Logs(QObject):
    def __init__(self, relative_datetime, datetime, sha, add_stats, del_stats):
        super().__init__()
        self.relative_datetime = relative_datetime
        self.datetime = datetime
        self.sha = sha
        self.add_stats = add_stats
        self.del_stats = del_stats
