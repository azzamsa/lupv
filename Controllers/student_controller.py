from PyQt5.QtCore import QObject
import git
from Model.logs import Logs


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
        # TODO get all the revision. non first revision is blank
        student_repo = self.get_student_repo()
        diff = student_repo.git.show(sha, '.watchers/auth_info')
        infos = diff.splitlines()[12:]
        auth_info = []
        for info in infos:
            if info != '':
                auth_info.append(info)
        return auth_info

    def read_all_windows(self, sha):
        # TODO remove git attribute
        student_repo = self.get_student_repo()
        diff = student_repo.git.show(sha, '.watchers/all_windows')
        diff_body = diff.splitlines()[14:]
        windows = []
        for line in diff_body:
            if line != '':
                windows.append(line)
        return windows

    def read_logs(self):
        """Read log form student directory"""
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
