import git
import editdistance
from os.path import join

from PyQt5.QtCore import QObject

from Model.logs import Logs


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

    def read_logs(self, selected_file=None):
        """Read log form student directory."""
        student_repo = self.get_student_repo()
        records = list(student_repo.iter_commits('master'))
        insertions = 0
        deletions = 0
        logs = []

        for rec in records:
            relative_datetime = self._controller.humanize_dateime(
                rec.committed_datetime)
            datetime = str(rec.committed_datetime).split('+')[0]
            sha = rec.hexsha

            # TODO use 1 variable instead of separated add and del
            if selected_file:
                file_existp = self.is_file_exist(selected_file, rec.hexsha)
                if file_existp:
                    insertions = rec.stats.files[selected_file]['insertions']
                    deletions = rec.stats.files[selected_file]['deletions']
                else:
                    insertions = 0
                    deletions = 0

            log = Logs(relative_datetime, datetime, sha, insertions, deletions)
            logs.append(log)

        return logs

    def is_file_exist(self, filename, sha):
        """Check if filename in current record exist."""
        student_repo = self.get_student_repo()
        files = student_repo.git.show('--pretty=' '', '--name-only', sha)
        if filename in files:
            return True
        else:
            return False

    def calc_editdistance_ax(self, selected_file):
        editdistance_ax = []
        records_count = 0
        records_ax = []
        ed_ax = []
        student_repo = self.get_student_repo()
        records = list(student_repo.iter_commits('master'))
        last_record_sha = records[0].hexsha

        if selected_file:
            last_file = student_repo.git.show('{}:{}'.format(
                last_record_sha, selected_file))

            for record in records:
                file_existp = self.is_file_exist(selected_file, record.hexsha)
                if file_existp:
                    current_file = student_repo.git.show('{}:{}'.format(
                        record.hexsha, selected_file))
                    ed = editdistance.eval(last_file, current_file)
                    ed_ax.append(ed)

                    records_count += 1
                    records_ax.append(records_count)

        editdistance_ax.append(records_ax)
        editdistance_ax.append(ed_ax)
        return editdistance_ax
