import os
import git
import pendulum
from os.path import join

from PyQt5.QtCore import QObject

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
            if os.path.isdir(join(record_path, d, '.git')):
                student_dirs.append(d)
            else:
                print('skipped' + d + '. Task not valid.')
        return student_dirs

    def get_files(self, record_path):
        dirs = os.listdir(record_path)
        files = []
        for d in dirs:
            if os.path.isfile(os.path.join(record_path, d)):
                files.append(d)
        return files

    def get_records(self, record_path):
        """Return list of records from individual directory."""
        repo = git.Repo(record_path)
        records = list(repo.iter_commits('master'))
        return records

    def calc_work_duration(self, record_path):
        """Calculate duration between last and first."""
        records = self.get_records(record_path)
        duration = []

        # last - first
        delta = records[0].committed_datetime - records[-1].committed_datetime
        duration.append(str(delta))

        dt_last = pendulum.instance(records[0].committed_datetime)
        dt_first = pendulum.instance(records[-1].committed_datetime)
        dt_delta = dt_last - dt_first
        duration.append(dt_delta.in_words(locale='en'))

        return duration

    def count_records(self, record_path):
        """Count the total amount of records."""
        records = self.get_records(record_path)
        return len(records)

    def get_last_rec_time(self, record_path):
        """Take the last record."""
        last_rec_time = []
        records = self.get_records(record_path)

        last_rec_dt = records[0].committed_datetime
        last_rec_time.append(str(last_rec_dt).split("+")[0])

        dt = pendulum.instance(last_rec_dt)
        last_rec_time.append(dt.diff_for_humans())

        return last_rec_time

    def get_first_rec_time(self, record_path):
        """Take the first record."""
        first_rec_time = []
        records = self.get_records(record_path)

        first_rec_dt = records[-1].committed_datetime
        first_rec_time.append(str(first_rec_dt).split("+")[0])

        dt = pendulum.instance(first_rec_dt)
        first_rec_time.append(dt.diff_for_humans())

        return first_rec_time

    def get_first_rec_sha(self, record_path):
        """Take the first SHA record."""
        records = self.get_records(record_path)
        return records[-1].hexsha

    def read_records(self, humanize=True):
        """Read records from individual dirs then return them as
        `Records` object."""
        rec_path = self._model.get_record_path()
        student_dirs = self.get_student_dirs(rec_path)
        records = []
        dt_type = 0

        if humanize:
            dt_type = 1

        for d in student_dirs:
            name = str(d).split("-")[0]
            nim = str(d).split("-")[1]
            student_path = join(rec_path, d)

            work_duration = self.calc_work_duration(student_path)
            record_amounts = self.count_records(student_path)
            first_rec = self.get_first_rec_time(student_path)
            last_record = self.get_last_rec_time(student_path)

            record = Records(name, nim, work_duration[dt_type], record_amounts,
                             first_rec[dt_type], last_record[dt_type])
            records.append(record)

        return records

    def humanize_dateime(self, datetime):
        dt = pendulum.instance(datetime)
        human_time = dt.diff_for_humans()
        return human_time
