import git

from PyQt5.QtCore import QObject

from Model.logs import Logs

# TODO highlight / pretteier git diff


class StudentController(QObject):

    def __init__(self, model, student_dir):
        super().__init__()

        self._model = model
        self._student_dir = student_dir

    def get_student_path(self):
        record_path = self._model.get_record_path()
        student_path = record_path + '/' + self._student_dir
        return student_path

    def get_student_repo(self):
        student_path = self.get_student_path()
        student_repo = git.Repo(student_path)
        return student_repo

    def read_auth_info(self, sha):
        student_repo = self.get_student_repo()

        auth_file = student_repo.git.show('{}:.watchers/auth_info'
                                          .format(sha))
        auth_info = auth_file.splitlines()
        return auth_info

    def read_all_windows(self, sha):
        student_repo = self.get_student_repo()
        diff = student_repo.git.show('{}:.watchers/all_windows'
                                     .format(sha))
        windows = diff.splitlines()
        return windows

    def read_focused_window(self, sha):
        student_repo = self.get_student_repo()
        focused_window = student_repo.git.show('{}:.watchers/focused_window'
                                               .format(sha))
        return focused_window

    def read_logs(self):
        """Read log form student directory."""
        student_repo = self.get_student_repo()
        records = list(student_repo.iter_commits('master'))
        logs = []

        for rec in records:
            name = rec.committer.name
            summary = rec.summary
            email = rec.committer.email
            sha = rec.hexsha
            log = Logs(name, summary, email, sha)
            logs.append(log)

        return logs
