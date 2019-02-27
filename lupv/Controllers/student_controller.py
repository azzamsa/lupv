import git
import editdistance as edlib
from os.path import join
import pathlib

from PyQt5.QtCore import QObject

from Model.logs import Logs


class StudentController(QObject):
    def __init__(self, controller, record_path, student_dir):
        super().__init__()

        self._controller = controller
        self._record_path = record_path
        self._student_dir = student_dir

    def get_student_path(self):
        """Construct student path from record_path and student_dir."""
        student_path = join(self._record_path, self._student_dir)
        return student_path

    def get_student_repo(self):
        """Initialize student repo."""
        student_path = self.get_student_path()
        student_repo = git.Repo(student_path)
        return student_repo

    def read_auth_info(self, sha):
        """Read auth_info from watchers"""
        student_repo = self.get_student_repo()
        auth_path = join(".watchers", "auth_info")
        auth_file = student_repo.git.show("{}:{}".format(sha, auth_path))
        auth_info = auth_file.splitlines()
        return auth_info

    def read_all_windows(self, sha):
        """Read all windows from watchers"""
        student_repo = self.get_student_repo()
        all_win_path = join(".watchers", "all_windows")
        diff = student_repo.git.show("{}:{}".format(sha, all_win_path))
        windows = diff.splitlines()
        return windows

    def read_focused_window(self, sha):
        """Read focused window from watchers"""
        student_repo = self.get_student_repo()
        foc_win_path = join(".watchers", "focused_window")
        focused_window = student_repo.git.show("{}:{}".format(sha, foc_win_path))
        return focused_window

    def read_logs(self, selected_file=None):
        """Read log form student directory."""
        student_path = self.get_student_path()
        records = self._controller.get_records(student_path)
        insertions = 0
        deletions = 0
        logs = []

        for rec in records:
            relative_datetime = self._controller.humanize_dateime(
                rec.committed_datetime
            )
            datetime = "{:%a, %d %b %Y, %H:%M:%S}".format(rec.committed_datetime)
            sha = rec.hexsha

            if selected_file:
                file_existp = self._controller.is_file_in_commit(selected_file, rec.hexsha)
                if file_existp:
                    insertions = rec.stats.files[selected_file]["insertions"]
                    deletions = rec.stats.files[selected_file]["deletions"]
                else:
                    insertions = 0
                    deletions = 0

            log = Logs(relative_datetime, datetime, sha, insertions, deletions)
            logs.append(log)

        return logs

    def read_file_content(self, selected_file, sha):
        "Read the content of current file state"
        student_repo = self.get_student_repo()
        file_existp = self._controller.is_file_in_commit(selected_file, sha)
        if file_existp:
            file_content = student_repo.git.show("{}:{}".format(sha, selected_file))
            return file_content

    def calc_editdistance_ax(self, selected_file):
        """Calculate EditDistance axis."""
        editdistance = []
        records_count = 0
        records_ax = []
        editdistance_ax = []

        student_repo = self.get_student_repo()

        student_path = self.get_student_path()
        student_repo = git.Repo(student_path)
        records = list(student_repo.iter_commits("master"))
        last_record_sha = records[0].hexsha

        if selected_file:
            last_file = student_repo.git.show(
                "{}:{}".format(last_record_sha, selected_file)
            )

            for record in records:
                file_existp = self._controller.is_file_in_commit(
                    student_repo, selected_file, record.hexsha
                )
                if file_existp:
                    current_file = student_repo.git.show(
                        "{}:{}".format(record.hexsha, selected_file)
                    )
                    ed = edlib.eval(last_file, current_file)
                    editdistance_ax.append(ed)

                    records_count += 1
                    records_ax.append(records_count)

        editdistance.append(records_ax)
        editdistance.append(editdistance_ax)
        return editdistance

    def create_lupvnotes_dir(self):
        """Create lupv-notes directory."""
        pathlib.Path(self._record_path + "/lupv-notes").mkdir(
            parents=True, exist_ok=True
        )

    def get_graph_path(self):
        graph_path = join(self._record_path, "lupv-notes", self._student_dir + ".png")
        return graph_path
