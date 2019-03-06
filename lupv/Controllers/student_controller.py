from os.path import join

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
        student_repo = self._controller.initialize_repo(student_path)
        return student_repo

    def get_student_records(self):
        """Return records of student"""
        student_path = self.get_student_path()
        records = self._controller.get_records(student_path)
        return records

    def diff_file(self, selected_file, sha, student_repo=None):
        """Get content of diff file."""
        student_repo = self.get_student_repo() if student_repo is None else student_repo
        file_diff = student_repo.git.show(sha, selected_file)
        return file_diff

    def read_focused_window(self, sha):
        """Read focused window from watchers."""
        student_repo = self.get_student_repo()
        foc_win_path = join(".watchers", "focused_window")
        focused_window = student_repo.git.show("{}:{}".format(sha, foc_win_path))
        return focused_window

    def get_auth_info(self, sha):
        auth_info = self._controller.read_auth_info(sha, self.get_student_repo())
        return auth_info

    def get_all_windows(self, sha):
        all_windows = self._controller.read_all_windows(sha, self.get_student_repo())
        return all_windows

    def read_logs(self, selected_file=None):
        """Read logs from student directory."""
        student_records = self.get_student_records()

        for rec in student_records:
            relative_time = self._controller.relativize_datetime(rec.committed_datetime)
            time = "{:%a, %d %b %Y, %H:%M:%S}".format(rec.committed_datetime)
            sha = rec.hexsha
            insertions = 0
            deletions = 0

            if selected_file:
                if self._controller.is_exists(
                    selected_file, sha, self.get_student_repo()
                ):
                    insertions = rec.stats.files[selected_file]["insertions"]
                    deletions = rec.stats.files[selected_file]["deletions"]

            log = Logs(relative_time, time, sha, insertions, deletions)
            yield log

    def take_diff_body(self, diff):
        """Remove header from diff."""
        lines = diff.splitlines()
        diff_body = lines[11:]
        return "\n".join(diff_body)

    def wrap_with_html(self, diff):
        """Add html-css element into diff."""
        colored_diff = []
        css = "<span style='color:{color};white-space:pre;'>{line}</span>"
        lines = diff.splitlines()
        for line in lines:
            if line.startswith("-"):
                colored_line = css.format(color="red", line=line)
            elif line.startswith("+"):
                colored_line = css.format(color="green", line=line)
            else:
                colored_line = line
            colored_diff.append(colored_line)
        return "<br/>".join(colored_diff)

    def read_file_content(self, selected_file, sha, mode):
        "Return the content of current file according to specified mode."
        if self._controller.is_exists(selected_file, sha, self.get_student_repo()):
            if mode == "show":
                file_content = self._controller.show_file(
                    selected_file, sha, self.get_student_repo()
                )
            else:
                dirty_diff = self.diff_file(selected_file, sha)
                diff_body = self.take_diff_body(dirty_diff)
                file_content = self.wrap_with_html(diff_body)

            return file_content

    def get_editdistance_values(self, selected_file):
        records = self.get_student_records()
        editdistances_ax, records_ax = self._controller.calc_editdistances(
            selected_file, records, self.get_student_repo()
        )
        return editdistances_ax, records_ax
