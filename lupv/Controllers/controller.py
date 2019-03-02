import os
import git
import pendulum
from os.path import join
from collections import defaultdict


from PyQt5.QtCore import QObject

from Model.records import Records
from Model.search import Suspects
from Model.search import IpGroup


class Controller(QObject):
    def __init__(self):
        super().__init__()

    def validate_path(self, path):
        """Validate chosen path.

        This is necessary because invalid path will break `read_records` and
        make application crash.
        """
        dirs = os.listdir(path)
        invalid_dirs = []
        for d in dirs:
            if d != "lupv-notes":
                if not os.path.isdir(join(path, d, ".git")):
                    invalid_dirs.append(d)

        return invalid_dirs

    def get_student_dirs(self, record_path):
        "Return list of student directories"
        dirs = os.listdir(record_path)
        student_dirs = []
        for d in dirs:
            if d != "lupv-notes":
                if os.path.isdir(join(record_path, d, ".git")):
                    student_dirs.append(d)
                else:
                    # TODO use log
                    print("skipped " + d + ". Task not valid.")
        return student_dirs

    def get_files(self, student_path):
        """Return list of files inside student directory."""
        dirs = os.listdir(student_path)
        files = []
        for d in dirs:
            if os.path.isfile(os.path.join(student_path, d)):
                files.append(d)
        return files

    def get_student_repo(self, student_path):
        student_repo = git.Repo(student_path)
        return student_repo

    def get_records(self, student_path):
        """Return list of records from individual directory."""
        student_repo = self.get_student_repo(student_path)
        records = list(student_repo.iter_commits("master"))
        return records

    def calc_work_duration(self, records):
        """Calculate duration between last and first."""
        duration = []

        # last - first
        delta = records[0].committed_datetime - records[-1].committed_datetime
        duration.append(str(delta))

        dt_last = pendulum.instance(records[0].committed_datetime)
        dt_first = pendulum.instance(records[-1].committed_datetime)
        dt_delta = dt_last - dt_first
        duration.append(dt_delta.in_words(locale="en"))

        return duration

    def count_records(self, records):
        """Count the total amount of records."""
        return len(records)

    def get_last_rec_time(self, records):
        """Take the last record."""
        last_rec_time = []

        last_rec_dt = records[0].committed_datetime
        last_rec_time.append("{:%a, %d %b %Y, %H:%M:%S}".format(last_rec_dt))

        dt = pendulum.instance(last_rec_dt)
        last_rec_time.append(dt.diff_for_humans())

        return last_rec_time

    def get_first_rec_time(self, records):
        """Take the first record."""
        first_rec_time = []

        first_rec_dt = records[-1].committed_datetime
        first_rec_time.append("{:%a, %d %b %Y, %H:%M:%S}".format(first_rec_dt))

        dt = pendulum.instance(first_rec_dt)
        first_rec_time.append(dt.diff_for_humans())

        return first_rec_time

    def get_first_rec_sha(self, records):
        """Take the first SHA record."""
        return records[-1].hexsha

    def read_records(self, record_path):
        """Read records from individual dirs then return them as
        `Records` object."""
        student_dirs = self.get_student_dirs(record_path)
        student_records = []

        for student in student_dirs:
            student_path = join(record_path, student)
            records = self.get_records(student_path)

            name = str(student).split("-")[0]
            nim = str(student).split("-")[1]
            work_duration = self.calc_work_duration(records)
            record_amounts = self.count_records(records)
            first_record = self.get_first_rec_time(records)
            last_record = self.get_last_rec_time(records)

            record = Records(
                name, nim, work_duration, record_amounts, first_record, last_record
            )
            student_records.append(record)

        return student_records

    def humanize_dateime(self, datetime):
        """Convert date time to relative version."""
        dt = pendulum.instance(datetime)
        human_time = dt.diff_for_humans()
        return human_time

    def is_file_in_commit(self, student_repo, filename, sha):
        """Check if filename in current record exist."""
        files = student_repo.git.show("--pretty=" "", "--name-only", sha)
        if filename in files:
            return True
        else:
            return False

    def get_suspects(self, record_path, insertions_limit, filename):
        suspects = []
        student_dirs = self.get_student_dirs(record_path)

        for student in student_dirs:
            student_path = join(record_path, student)
            student_repo = self.get_student_repo(student_path)
            records = self.get_records(student_path)

            for rec in records:
                file_existp = self.is_file_in_commit(student_repo, filename, rec.hexsha)
                if file_existp:
                    insertions = rec.stats.files[filename]["insertions"]
                    if insertions > insertions_limit:
                        name = str(student).split("-")[0]
                        nim = str(student).split("-")[1]
                        date = "{:%a, %d %b %Y, %H:%M:%S}".format(
                            rec.committed_datetime
                        )
                        suspect = Suspects(name, nim, filename, insertions, date)
                        suspects.append(suspect)

        return suspects

    #
    # Search
    #

    def get_student_sample(self, record_path):
        students = self.get_student_dirs(record_path)
        student_sample_path = join(record_path, students[0])
        return student_sample_path

    def get_sample_file(self, student_sample_path):
        files = self.get_files(student_sample_path)
        return files

    def construct_parentchild(self, suspects):
        suspect_parentchild = defaultdict(list)
        # construct keys
        for suspect in suspects:
            key = "{}-{}".format(suspect.name, suspect.nim)
            suspect_parentchild[key].append(suspect)
        return suspect_parentchild

    def read_ips(self, record_path):
        student_and_ip = []
        student_dirs = self.get_student_dirs(record_path)

        for student in student_dirs:
            student_path = join(record_path, student)
            student_repo = self.get_student_repo(student_path)
            records = self.get_records(student_path)

            for rec in records:
                auth_path = join(".watchers", "auth_info")
                auth_file = student_repo.git.show("{}:{}".format(rec.hexsha, auth_path))
                ip = auth_file.splitlines()[2]

                name = str(student).split("-")[0]
                nim = str(student).split("-")[1]
                date = "{:%a, %d %b %Y, %H:%M:%S}".format(rec.committed_datetime)
                ip_group = IpGroup(ip, name, nim, date)
                student_and_ip.append(ip_group)

        return student_and_ip

    def group_by_ip(self, student_and_ip):
        # construct ip : students
        student_group = defaultdict(list)
        for student in student_and_ip:
            ip = "{}".format(student.ip)
            student_group[ip].append(student)

        ip_student_students = {}
        # construct ip : student : students
        for key in student_group.keys():
            models = student_group[key]
            student_students = defaultdict(list)
            for model in models:
                student_key = "{}-{}".format(model.name, model.nim)
                student_students[student_key].append(model)
            ip_student_students[key] = student_students
        return ip_student_students
