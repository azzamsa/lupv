import os
import git
import pendulum
from os.path import join
import pathlib
import editdistance as edlib


from PyQt5.QtCore import QObject

from Model.records import Records


class Controller(QObject):
    def __init__(self):
        super().__init__()
        self._record_path = ""

    def create_lupvnotes_dir(self, record_path):
        """Create lupv-notes directory."""
        pathlib.Path(record_path + "/lupv-notes").mkdir(parents=True, exist_ok=True)

    def is_student_dir(self, path):
        """Check if path contain valid student directory.

        This is necessary because invalid directory will break `read_records` and
        make application crash.
        """
        dirs = os.listdir(path)
        invalid_student_dirs = []
        for d in dirs:
            if d != "lupv-notes":
                if not os.path.isdir(join(path, d, ".git")):
                    invalid_student_dirs.append(d)

        return invalid_student_dirs

    def get_student_dirs(self, record_path):
        "Return list of student directories"
        dirs = os.listdir(record_path)
        student_dirs = []
        for d in dirs:
            if d != "lupv-notes":
                if os.path.isdir(join(record_path, d, ".git")):
                    student_dirs.append(d)
        return student_dirs

    def get_files(self, student_path):
        """Return files in student directory."""
        dirs = os.listdir(student_path)
        files = []
        for d in dirs:
            if os.path.isfile(os.path.join(student_path, d)):
                files.append(d)
        return files

    def initialize_repo(self, path):
        """Initialize student repo."""
        repo = git.Repo(path)
        return repo

    def get_records(self, student_path):
        """Return records from student directory."""
        student_repo = git.Repo(student_path)
        records = list(student_repo.iter_commits("master"))
        return records

    def relativize_datetime(self, datetime):
        """Convert datetime into its relative version."""
        dt = pendulum.instance(datetime)
        relative_time = dt.diff_for_humans()
        return relative_time

    def get_first_record_time(self, first_record_dt):
        """Take the first record time."""
        first_record_time = "{:%a, %d %b %Y, %H:%M:%S}".format(first_record_dt)
        first_record_relativetime = self.relativize_datetime(first_record_dt)
        return first_record_time, first_record_relativetime

    def get_last_record_time(self, last_record_dt):
        """Take the last record time."""
        last_record_time = "{:%a, %d %b %Y, %H:%M:%S}".format(last_record_dt)
        last_record_relativetime = self.relativize_datetime(last_record_dt)
        return last_record_time, last_record_relativetime

    def calc_work_duration(self, first_record_dt, last_record_dt):
        """Calculate duration between last and first record time."""
        work_duration = str(last_record_dt - first_record_dt)
        last_dt, first_dt = [
            pendulum.instance(x) for x in [last_record_dt, first_record_dt]
        ]
        work_relative_duration = (last_dt - first_dt).in_words(locale="en")
        return work_duration, work_relative_duration

    def read_records(self, record_path):
        """Read records from student directories."""
        student_dirs = self.get_student_dirs(record_path)
        self._record_path = record_path

        for student in student_dirs:
            student_path = join(record_path, student)
            records = self.get_records(student_path)
            first_record_dt, last_record_dt = [
                records[x].committed_datetime for x in [-1, 0]
            ]
            name, student_id = [str(student).split("-")[x] for x in [0, 1]]

            total_records = len(records)
            first_record_time, first_record_relativetime = self.get_first_record_time(
                first_record_dt
            )
            last_record_time, last_record_relativetime = self.get_last_record_time(
                last_record_dt
            )
            work_duration, work_relative_duration = self.calc_work_duration(
                first_record_dt, last_record_dt
            )

            record = Records(
                name,
                student_id,
                total_records,
                first_record_time,
                first_record_relativetime,
                last_record_time,
                last_record_relativetime,
                work_duration,
                work_relative_duration,
            )
            yield record

    def is_exists(self, filename, sha, student_repo=None):
        """Check if filename in current record exist."""
        files = student_repo.git.show("--pretty=" "", "--name-only", sha)
        if filename in files:
            return True

    def read_auth_info(self, sha, student_repo):
        """Read auth_info from watchers."""
        auth_path = join(".watchers", "auth_info")
        auth_file = student_repo.git.show("{}:{}".format(sha, auth_path))
        auth_info = auth_file.splitlines()
        return auth_info

    def read_all_windows(self, sha, student_repo):
        """Read all windows from watchers."""
        all_win_path = join(".watchers", "all_windows")
        diff = student_repo.git.show("{}:{}".format(sha, all_win_path))
        windows = diff.splitlines()
        return windows

    def show_file(self, selected_file, sha, student_repo):
        """Get content of current file state."""
        current_file = student_repo.git.show("{}:{}".format(sha, selected_file))
        return current_file

    def calc_editdistances(self, selected_file, records, student_repo):
        """Calculate editdistance and record axis."""
        records_count = 0
        records_ax = []
        editdistances_ax = []

        # records = self.get_student_records()
        last_record_sha = records[0].hexsha
        last_file = self.show_file(selected_file, last_record_sha, student_repo)

        for record in records:
            if self.is_exists(selected_file, record.hexsha, student_repo):
                current_file = self.show_file(
                    selected_file, record.hexsha, student_repo
                )
                editdistance_value = edlib.eval(last_file, current_file)
                editdistances_ax.append(editdistance_value)

                records_count += 1
                records_ax.append(records_count)

        return editdistances_ax, records_ax

    # ini di search contrioller seharusnya
    def get_editdistance_values(self, selected_file, student):
        student_path = join(self._record_path, student)
        records = self.get_records(student_path)
        student_repo = self.initialize_repo(student_path)
        editdistances_ax, records_ax = self.calc_editdistances(
            selected_file, records, student_repo
        )
        return editdistances_ax, records_ax
