from PyQt5.QtCore import QObject


class Records(QObject):
    def __init__(
        self,
        name,
        nim,
        total_records,
        work_duration,
        first_record,
        last_record,
        rel_work_duration,
        rel_first_record,
        rel_last_record,
    ):
        super().__init__()
        self.name = name
        self.nim = nim
        self.total_records = total_records
        self.work_duration = work_duration
        self.first_record = first_record
        self.last_record = last_record
        self.rel_work_duration = rel_work_duration
        self.rel_first_record = rel_first_record
        self.rel_last_record = rel_last_record
