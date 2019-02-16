from PyQt5.QtCore import QObject
import os
import git
from Model.records import Records


class Controller(QObject):

    def __init__(self, model):
        super().__init__()

        self._model = model

    def save_record_path(self, record_path):
        "save task path to model"
        self._model.set_record_path(record_path)

    def get_student_dirs(self, record_path):
        "Return list of student directories"
        dirs = os.listdir(record_path)
        student_dirs = []
        for d in dirs:
            if os.path.isdir(record_path + '/' + d + '/.git'):
                student_dirs.append(d)
            else:
                print('skipped' + d + '. Task not valid.')
        return student_dirs

    def get_name(self, path):
        pass

    def get_nim(self, path):
        pass

    def get_records(self, record_path):
        """Return list of records from individual directory"""
        repo = git.Repo(record_path)
        records = list(repo.iter_commits('master'))
        return records

    def calc_work_duration(self, record_path):
        """Calculate duration between first and last commit"""
        records = self.get_records(record_path)
        dates = []

        for r in records:
            dates.append(r.committed_datetime)

        first_records = dates[0]
        last_records = dates[-1]
        duration = first_records - last_records
        return duration

    def count_records(self, record_path):
        """Count the total amount of records"""
        records = self.get_records(record_path)
        return len(records)

    def get_last_record(self, record_path):
        """Take the last record"""
        records = self.get_records(record_path)
        last_record = str(records[0].committed_datetime).split("+")[0]
        return last_record

    def get_first_record(self, record_path):
        """Take the first record"""
        records = self.get_records(record_path)
        first_record = str(records[-1].committed_datetime).split("+")[0]
        return first_record

    def read_records(self, record_path):
        """Read records from individual dirs then return them as
        `Records` object"""
        rec_path = record_path
        student_dirs = self.get_student_dirs(rec_path)
        records = []

        for d in student_dirs:
            name = str(d).split("-")[0]
            nim = str(d).split("-")[1]
            work_duration = self.calc_work_duration(rec_path + "/" + d)
            record_amounts = self.count_records(rec_path + "/" + d)
            first_record = self.get_first_record(rec_path + "/" + d)
            last_record = self.get_last_record(rec_path + "/" + d)
            record = Records(name, nim, work_duration, record_amounts,
                             first_record, last_record)
            records.append(record)

        return records
