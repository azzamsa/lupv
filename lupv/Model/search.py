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


class StudentWindow(QObject):
    def __init__(self, window_name, name, nim, date):
        super().__init__()
        self.window_name = window_name
        self.name = name
        self.nim = nim
        self.date = date


class StudentEditDistance(QObject):
    def __init__(self, name, nim, editdistance_ax, records_ax, task_name):
        super().__init__()
        self.name = name
        self.nim = nim
        self.editdistance_ax = editdistance_ax
        self.records_ax = records_ax
        self.task_name = task_name
