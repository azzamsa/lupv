from PyQt5.QtCore import QObject


class Suspects(QObject):
    def __init__(self, name, nim, filename, insertions, date):
        super().__init__()
        self.name = name
        self.nim = nim
        self.filename = filename
        self.insertions = insertions
        self.date = date


class IpGroup(QObject):
    def __init__(self, ip, name, nim, date):
        super().__init__()
        self.ip = ip
        self.name = name
        self.nim = nim
        self.date = date
