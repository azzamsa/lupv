from PyQt5.QtCore import QObject


class Records(QObject):
    def __init__(self, name, nim, work_duration, record_amounts,
                 first_record, last_record):
        super().__init__()
        self.name = name
        self.nim = nim
        self.work_duration = work_duration
        self.record_amounts = record_amounts
        self.last_record = last_record
        self.first_record = first_record
