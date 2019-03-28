import editdistance as edlib

from PyQt5.QtCore import QObject


class LogController(QObject):
    def __init__(self, main_ctrl, log_model):
        super().__init__()

        self._main_ctrl = main_ctrl
        self._log_model = log_model

    def change_current_student_dir(self, current_student_dir):
        self._log_model.current_student_dir = current_student_dir

    def change_record_path(self, record_path):
        """Change record path value."""
        self._log_model.record_path = record_path

    def populate_logs(self, selected_file=None):
        """Return student's log."""
        student_records = self._log_model.student_records

        for record in student_records:
            relative_time = self._main_ctrl.relativize_datetime(
                record.committed_datetime
            )
            time_format = "{:%a, %d %b %Y, %H:%M:%S}"
            time = time_format.format(record.committed_datetime)
            sha = record.hexsha
            insertions = 0
            deletions = 0

            if selected_file:
                if self._log_model.is_exists(selected_file, sha):
                    insertions = record.stats.files[selected_file]["insertions"]
                    deletions = record.stats.files[selected_file]["deletions"]

            log = dict(
                relative_time=relative_time,
                time=time,
                sha=sha,
                insertions=insertions,
                deletions=deletions,
            )
            yield log

    def populate_files(self):
        """Return list of files."""
        files = self._log_model.read_files()
        return files

    def populate_auth_info(self, sha):
        """Return student's auth information."""
        auth_info = self._log_model.read_auth_info(sha)
        return auth_info

    def populate_all_windows(self, sha):
        """Return all student's window name."""
        all_windows = self._log_model.read_all_windows(sha)
        return all_windows

    def populate_focused_window(self, sha):
        """Return focused window name."""
        focused = self._log_model.read_focused_window(sha)
        return focused

    def take_diff_body(self, diff):
        """Remove header from diff."""
        # FIXME use regex
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

    def get_diff(self, filename, sha):
        dirty_diff = self._log_model.read_diff(filename, sha)
        diff_body = self.take_diff_body(dirty_diff)
        file_content = self.wrap_with_html(diff_body)
        return file_content

    def populate_file_content(self, filename, sha, mode="show"):
        "Return the content of current file according to specified mode."
        if self._log_model.is_exists(filename, sha):
            file_content = self._log_model.read_file(filename, sha)
            if mode == "diff":
                file_content = self.get_diff(filename, sha)

            return file_content
