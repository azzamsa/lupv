import pytest
import os.path as osp
from datetime import datetime, timedelta

from Lupv.models.main import MainModel
from Lupv.controllers.main import MainController
from Lupv.models.logs import LogModel
from Lupv.controllers.log import LogController
from tests.helper import fixture


class TestMainController:
    @pytest.fixture
    def main_ctrl_model(self):
        main_model = MainModel()
        main_model.record_path_changed.disconnect(main_model.read_students_records)
        main_ctrl = MainController(main_model)
        return main_ctrl, main_model

    @pytest.fixture
    def main_ctrl(self):
        main_model = MainModel()
        main_ctrl = MainController(main_model)
        return main_ctrl

    def test_setters(self, main_ctrl_model):
        main_ctrl, main_model = main_ctrl_model
        record_path = "home/x/student_tasks"
        main_ctrl.change_record_path(record_path)

        assert main_model.record_path == "home/x/student_tasks"

    def test_validate(self, main_ctrl):
        record_path = osp.join(osp.dirname(__file__), "student_tasks")
        invalid_dirs = main_ctrl.validate(record_path)
        assert not invalid_dirs

    def test_validate_invalid_dir(self, main_ctrl, fs):
        fs.create_dir("home/x/student_tasks/ani-1111/.git")
        fs.create_dir("home/x/student_tasks/budi-2222/.git")
        fs.create_dir("home/x/student_tasks/lupv-notes")
        fs.create_dir("home/x/student_tasks/invalid-3333")

        invalid_dirs = main_ctrl.validate("home/x/student_tasks")
        assert "invalid-3333" == invalid_dirs[0]

    def test_relativize_datetime(self, main_ctrl):
        # datetime.now() didn't work, must use utcnow()
        dt = datetime.utcnow() - timedelta(hours=1)
        relative_time = main_ctrl.relativize_datetime(dt)

        assert "ago" in relative_time

    def test_get_first_record_time(self, main_ctrl):
        dt = datetime.utcnow() - timedelta(hours=1)
        first_time, first_relative_time = main_ctrl.get_first_record_time(dt)

        current_time = "{:%a, %d %b %Y}".format(dt)
        assert current_time in first_time
        assert "ago" in first_relative_time

    def test_get_last_record_time(self, main_ctrl):
        dt = datetime.utcnow() - timedelta(hours=1)
        first_time, first_relative_time = main_ctrl.get_last_record_time(dt)

        current_time = "{:%a, %d %b %Y}".format(dt)
        assert current_time in first_time
        assert "ago" in first_relative_time

    def test_calc_work_duration(self, main_ctrl):
        first_dt = datetime.utcnow() - timedelta(hours=1)
        last_dt = datetime.utcnow() - timedelta(hours=-1)
        work_duration, work_relative_duration = main_ctrl.calc_work_duration(
            first_dt, last_dt
        )

        assert "2" in work_duration
        assert "2 hours" in work_relative_duration

    def test_populate_students_records(self, main_ctrl_model):
        main_ctrl, main_model = main_ctrl_model
        record_path = osp.join(osp.dirname(__file__), "student_tasks")
        main_model.record_path = record_path
        main_model.read_students_records()

        student_records = []
        for student_record in main_ctrl.populate_students_records():
            student_records.append(student_record)
            if student_record["name"] == "ani":
                ani_record = student_record
            if student_record["name"] == "budi":
                budi_record = student_record

        assert len(student_records) == 2

        assert ani_record["name"] == "ani"
        assert ani_record["student_id"] == "1111"
        assert ani_record["total_records"] == 4
        assert ani_record["first_record_time"] == "Tue, 26 Mar 2019, 13:52:38"
        assert ani_record["first_record_relativetime"] == "2 days ago"
        assert ani_record["last_record_time"] == "Tue, 26 Mar 2019, 13:52:48"
        assert ani_record["last_record_relativetime"] == "2 days ago"
        assert ani_record["work_duration"] == "0:00:10"
        assert ani_record["work_relative_duration"] == "10 seconds"

        assert budi_record["name"] == "budi"
        assert budi_record["student_id"] == "2222"
        assert budi_record["total_records"] == 4
        assert budi_record["first_record_time"] == "Tue, 26 Mar 2019, 14:08:18"
        assert budi_record["first_record_relativetime"] == "2 days ago"
        assert budi_record["last_record_time"] == "Tue, 26 Mar 2019, 14:08:30"
        assert budi_record["last_record_relativetime"] == "2 days ago"
        assert budi_record["work_duration"] == "0:00:12"
        assert budi_record["work_relative_duration"] == "12 seconds"


class TestLogController:
    @pytest.fixture
    def log_ctrl(self):
        main_model = MainModel()
        main_model.record_path_changed.disconnect(main_model.read_students_records)
        log_model = LogModel(main_model)
        log_model.current_student_dir_changed.disconnect(
            log_model.on_current_student_dir_changed
        )
        main_ctrl = MainController(main_model)
        log_ctrl = LogController(main_ctrl, log_model)

        record_path = osp.join(osp.dirname(__file__), "student_tasks")
        student_path = osp.join(record_path, "ani-1111")
        log_model.record_path = record_path
        log_model.current_student_dir = "ani-1111"
        log_model.student_path = student_path
        log_model.on_current_student_dir_changed()

        return log_ctrl

    def test_setters(self):
        main_model = MainModel()
        main_model.record_path_changed.disconnect(main_model.read_students_records)
        log_model = LogModel(main_model)
        log_model.current_student_dir_changed.disconnect(
            log_model.on_current_student_dir_changed
        )
        main_ctrl = MainController(main_model)
        log_ctrl = LogController(main_ctrl, log_model)

        student_dir = "ani-1111"
        log_ctrl.change_current_student_dir(student_dir)

        record_path = "home/x/student_tasks"
        log_ctrl.change_record_path(record_path)

        assert log_model.current_student_dir == "ani-1111"
        assert log_model.record_path == "home/x/student_tasks"

    def test_populate_logs(self, log_ctrl):
        ani_logs = []
        for log in log_ctrl.populate_logs(selected_file="tugas-tif.txt"):
            ani_logs.append(log)

        ani_log = ani_logs[0]
        assert ani_log["relative_time"] == "2 days ago"
        assert ani_log["time"] == "Tue, 26 Mar 2019, 13:52:48"
        assert ani_log["sha"] == "991dcb1ae434ffba832c0ad50b890afac7310608"
        assert ani_log["insertions"] == 1
        assert ani_log["deletions"] == 0

    def test_populate_files(self, log_ctrl):
        files = log_ctrl.populate_files()
        assert files[0] == "tugas-tif.txt"

    def test_populate_auth_info(self, log_ctrl):
        sha = "991dcb1ae434ffba832c0ad50b890afac7310608"
        auth_info = log_ctrl.populate_auth_info(sha)
        assert auth_info == ["ani", "ani-machine", "111.111.111"]

    def test_populate_all_windows(self, log_ctrl):
        sha = "991dcb1ae434ffba832c0ad50b890afac7310608"
        all_windows = log_ctrl.populate_all_windows(sha)
        assert all_windows == [
            "emacs@screencast",
            "FrontPage - Python Wiki - Firefox Developer Edition",
            "bash",
        ]

    def test_populate_focused_window(self, log_ctrl):
        sha = "991dcb1ae434ffba832c0ad50b890afac7310608"
        focused_window = log_ctrl.populate_focused_window(sha)
        assert focused_window == "bash"

    def test_take_diff_body(self, log_ctrl):
        ani_diff = fixture("ani_diff").decode()
        body = log_ctrl.take_diff_body(ani_diff)

        body_real = " ani 1\n+ani 2"
        assert body == body_real

    def test_wrap_with_html(self, log_ctrl):
        diff = "- ani 1\n+ani 2"
        colored_diff = log_ctrl.wrap_with_html(diff)

        colored_diff_real = fixture("colored_diff").decode()
        assert colored_diff == colored_diff_real

    def test_get_diff(self, log_ctrl):
        sha = "991dcb1ae434ffba832c0ad50b890afac7310608"
        file_content = log_ctrl.get_diff("tugas-tif.txt", sha)
        file_content_real = (
            " ani 1<br/><span style='color:green;white-space:pre;'>+ani 2</span>"
        )
        assert file_content == file_content_real

    def test_populate_file_content(self, log_ctrl):
        sha = "991dcb1ae434ffba832c0ad50b890afac7310608"
        file_content_show = log_ctrl.populate_file_content("tugas-tif.txt", sha)
        file_content_show_real = "ani 1\nani 2"

        file_content_diff = log_ctrl.populate_file_content(
            "tugas-tif.txt", sha, mode="diff"
        )
        file_content_diff_real = (
            " ani 1<br/><span style='color:green;white-space:pre;'>+ani 2</span>"
        )

        assert file_content_show == file_content_show_real
        assert file_content_diff == file_content_diff_real
