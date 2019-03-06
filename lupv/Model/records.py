from PyQt5.QtCore import QObject


class Records(QObject):
    def __init__(
        self,
        name,
        student_id,
        total_records,
        first_record_time,
        first_record_relativetime,
        last_record_time,
        last_record_relativetime,
        work_duration,
        work_relative_duration,
    ):
        super().__init__()
        self.name = name
        self.student_id = student_id
        self.total_records = total_records
        self.first_record_time = first_record_time
        self.first_record_relativetime = first_record_relativetime
        self.last_record_time = last_record_time
        self.last_record_relativetime = last_record_relativetime
        self.work_duration = work_duration
        self.work_relative_duration = work_relative_duration
