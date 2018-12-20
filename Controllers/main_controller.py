from PyQt5.QtCore import QObject
import os
import git
from Model.records import Records


class MainController(QObject):

    def __init__(self, model):
        super().__init__()

        self._model = model

    def set_record_dir(self, record_dir):
        self._model.set_record_dir(record_dir)

    def get_students_dir(self, root_dir):
        return os.listdir(root_dir)

    def get_name(self, dir_path):
        pass

    def get_nim(self, dir_path):
        pass

    def get_commits(self, dir_path):
        repo = git.Repo(dir_path)
        commits = list(repo.iter_commits('master'))
        return commits

    def get_work_duration(self, dir_path):
        commits = self.get_commits(dir_path)
        dates = []

        for c in commits:
            dates.append(c.committed_datetime)

        first_commit = dates[0]
        last_commit = dates[-1]
        duration = first_commit - last_commit
        return duration

    def get_record_amounts(self, dir_path):
        commits = self.get_commits(dir_path)
        records_amount = len(commits)
        return records_amount

    def get_last_record(self, dir_path):
        commits = self.get_commits(dir_path)
        last_record = str(commits[0].committed_datetime).split("+")[0]
        return last_record

    def get_first_record(self, dir_path):
        commits = self.get_commits(dir_path)
        first_record = str(commits[-1].committed_datetime).split("+")[0]
        return first_record

    def create_records(self):
        root_dir = self._model.get_record_dir()
        students = self.get_students_dir(root_dir)
        records = []

        for student in students:
            name = str(student).split("-")[0]
            nim = str(student).split("-")[1]
            work_duration = self.get_work_duration(root_dir + "/" + student)
            record_amounts = self.get_record_amounts(root_dir + "/" + student)
            first_record = self.get_first_record(root_dir + "/" + student)
            last_record = self.get_last_record(root_dir + "/" + student)
            name = Records(name, nim, work_duration, record_amounts,
                           first_record, last_record)
            records.append(name)

        return records
