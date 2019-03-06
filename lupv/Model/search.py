from PyQt5.QtCore import QObject


class Suspects(QObject):
    def __init__(self, name, student_id, filename, insertions, date):
        super().__init__()
        self.name = name
        self.student_id = student_id
        self.filename = filename
        self.insertions = insertions
        self.date = date


class IpGroup(QObject):
    def __init__(self, ip, name, student_id, date):
        super().__init__()
        self.ip = ip
        self.name = name
        self.student_id = student_id
        self.date = date


class StudentWindow(QObject):
    def __init__(self, window_name, student_name, student_id, date):
        super().__init__()
        self.window_name = window_name
        self.student_name = student_name
        self.student_id = student_id
        self.date = date


class StudentEditDistance(QObject):
    def __init__(self, name, student_id, editdistances_ax, records_ax, task_name):
        super().__init__()
        self.name = name
        self.student_id = student_id
        self.editdistances_ax = editdistances_ax
        self.records_ax = records_ax
        self.task_name = task_name
