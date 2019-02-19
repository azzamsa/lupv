import git
from os.path import join

from PyQt5.QtCore import QObject

from Model.logs import Logs

# TODO highlight / pretteier git diff


class StudentController(QObject):
    def __init__(self, model, controller, student_dir):
        super().__init__()

        self._model = model
        self._controller = controller
        self._student_dir = student_dir

    def get_student_path(self):
        record_path = self._model.get_record_path()
        student_path = join(record_path, self._student_dir)
        return student_path

    def get_student_repo(self):
        student_path = self.get_student_path()
        student_repo = git.Repo(student_path)
        return student_repo

    def read_auth_info(self, sha):
        student_repo = self.get_student_repo()
        auth_path = join('.watchers', 'auth_info')
        auth_file = student_repo.git.show('{}:{}'.format(sha, auth_path))
        auth_info = auth_file.splitlines()
        return auth_info

    def read_all_windows(self, sha):
        student_repo = self.get_student_repo()
        all_win_path = join('.watchers', 'all_windows')
        diff = student_repo.git.show('{}:{}'.format(sha, all_win_path))
        windows = diff.splitlines()
        return windows

    def read_focused_window(self, sha):
        student_repo = self.get_student_repo()
        foc_win_path = join('.watchers', 'focused_window')
        focused_window = student_repo.git.show('{}:{}'.format(
            sha, foc_win_path))
        return focused_window

    def read_logs(self):
        """Read log form student directory."""
        student_repo = self.get_student_repo()
        records = list(student_repo.iter_commits('master'))
        logs = []

        for rec in records:
            relative_datetime = self._controller.humanize_dateime(
                rec.committed_datetime)
            datetime = str(rec.committed_datetime).split('+')[0]
            sha = rec.hexsha
            log = Logs(relative_datetime, datetime, sha)
            logs.append(log)

        return logs
