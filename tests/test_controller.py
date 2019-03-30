import pytest
import os.path as osp

from Lupv.models.main import MainModel
from Lupv.controllers.main import MainController
from Lupv.models.logs import LogModel
from Lupv.controllers.log import LogController
from tests.helper import fixture
from tests.fixtures import record_fixture
from tests.fakes import controller_fake as cf


class TestMainController:
    @pytest.fixture
    def main_ctrl_model(self):
        """MainController fixture.
        Create MainController instance and disconnect all signal.

        :return: both main_ctrl and main_model because some function need both of them.
        """
        main_model = MainModel()
        main_model.record_path_changed.disconnect(main_model.read_students_records)
        main_ctrl = MainController(main_model)
        return main_ctrl, main_model

    @pytest.fixture
    def main_ctrl(self):
        """MainController fixture.
        Create MainController instance without disconnecting all signal.
        """
        main_model = MainModel()
        main_ctrl = MainController(main_model)
        return main_ctrl

    def test_property(self, main_ctrl_model):
        """Test MainController properties with dummy data."""
        main_ctrl, main_model = main_ctrl_model
        record_path = "home/x/student_tasks"
        main_ctrl.change_record_path(record_path)

        assert main_model.record_path == "home/x/student_tasks"

    def test_validate(self, main_ctrl):
        """Test checking valid directories using real data.

        :note: it's faster using real data than dummy filesystem
            real: 0.2s, fake: 0.5s."""
        record_path = osp.join(osp.dirname(__file__), "student_tasks")
        invalid_dirs = main_ctrl.validate(record_path)
        assert not invalid_dirs

    def test_validate_invalid_dir(self, main_ctrl, fs, monkeypatch):
        """Test checking valid directories using dummy filesystem.

        :note: using monkeypatch and pyfakefs is the same as taking 0.05s."""
        fs.create_dir("home/x/student_tasks/ani-1111/.git")
        fs.create_dir("home/x/student_tasks/budi-2222/.git")
        fs.create_dir("home/x/student_tasks/lupv-notes")
        fs.create_dir("home/x/student_tasks/invalid-3333")

        invalid_dirs = main_ctrl.validate("home/x/student_tasks")

        assert "invalid-3333" == invalid_dirs[0]

    def test_relativize_datetime(self, main_ctrl):
        """Test convertion datetime to its relative version using dummy data."""
        relative_time = main_ctrl.relativize_datetime(cf.sample_delta_dt)

        assert "ago" in relative_time

    def test_get_first_record_time(self, main_ctrl):
        """Test converting first.committed_datetime to human readable format
        and its relative version using dummy data."""
        dt = cf.sample_delta_dt
        first_time, first_relative_time = main_ctrl.get_first_record_time(dt)

        current_time = "{:%a, %d %b %Y}".format(dt)
        assert current_time in first_time
        assert "ago" in first_relative_time

    def test_get_last_record_time(self, main_ctrl):
        """Test converting last.committed_datetime to human readable format
        and its relative version using dummy data."""
        dt = cf.sample_delta_dt
        first_time, first_relative_time = main_ctrl.get_last_record_time(dt)

        current_time = "{:%a, %d %b %Y}".format(dt)
        assert current_time in first_time
        assert "ago" in first_relative_time

    def test_calc_work_duration(self, main_ctrl):
        """Test calculating delta between datetimes using dummy data."""
        first_dt = cf.sample_delta_dt
        last_dt = cf.sample_delta_dt_2
        work_duration, work_relative_duration = main_ctrl.calc_work_duration(
            first_dt, last_dt
        )

        assert "2" in work_duration
        assert "2 hours" in work_relative_duration

    def test_populate_students_records(self, main_ctrl_model):
        """Test populating students record using dummy data.

        :note: all faked function has been tested before.
        """
        main_ctrl, main_model = main_ctrl_model

        main_model.students_records = record_fixture.student_records_2
        main_ctrl.get_first_record_time = cf.fake_get_first_record_time
        main_ctrl.get_last_record_time = cf.fake_get_last_record_time
        main_ctrl.calc_work_duration = cf.fake_calc_work_duration

        student_records = list(main_ctrl.populate_students_records())

        budi_record = student_records[0]
        ani_record = student_records[1]
        assert len(student_records) == 2

        assert ani_record["name"] == "ani"
        assert ani_record["student_id"] == "1111"

        assert budi_record["name"] == "budi"
        assert budi_record["student_id"] == "2222"
        assert budi_record["total_records"] == 3
        assert budi_record["first_record_time"] == "Tue, 26 Mar 2019, 13:52:38"
        assert "ago" in budi_record["first_record_relativetime"]
        assert budi_record["last_record_time"] == "Tue, 26 Mar 2019, 13:52:48"
        assert "ago" in budi_record["last_record_relativetime"]
        assert budi_record["work_duration"] == "0:00:10"
        work_rel = "10 seconds"
        assert budi_record["work_relative_duration"] == work_rel


class TestLogController:
    @pytest.fixture
    def log_ctrl_model(self):
        """LogController fixture.
        Create LogController instance and disconnect all signal.

        :return: both log_ctrl and log_model because some function need both of them.
        """
        main_model = MainModel()
        main_model.record_path_changed.disconnect(main_model.read_students_records)
        log_model = LogModel(main_model)
        log_model.current_student_dir_changed.disconnect(
            log_model.on_current_student_dir_changed
        )
        main_ctrl = MainController(main_model)
        log_ctrl = LogController(main_ctrl, log_model)

        return log_ctrl, log_model

    @pytest.fixture
    def log_ctrl(self):
        """LogController fixture.
        Create LogController instance and disconnect all signal.
        """
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
        log_model.current_student_dir = "ani-1111"  # use ani only for this test
        log_model.student_path = student_path
        log_model.on_current_student_dir_changed()

        return log_ctrl

    def test_property(self, log_ctrl_model):
        """Test LogController properties using dummy data."""
        log_ctrl, log_model = log_ctrl_model
        student_dir = "ani-1111"
        log_ctrl.change_current_student_dir(student_dir)

        record_path = "home/x/student_tasks"
        log_ctrl.change_record_path(record_path)

        assert log_model.current_student_dir == "ani-1111"
        assert log_model.record_path == "home/x/student_tasks"

    def test_populate_logs(self, log_ctrl_model):
        """Test populating student logs using dummy data."""
        log_ctrl, log_model = log_ctrl_model
        log_model.student_records = record_fixture.student_records
        log_model.is_exists = cf.fake_is_exists

        ani_logs = list(log_ctrl.populate_logs(selected_file="tugas-tif.txt"))

        ani_log = ani_logs[0]
        assert "ago" in ani_log["relative_time"]
        assert ani_log["time"] == "Sat, 30 Mar 2019, 01:00:57"
        assert ani_log["sha"] == "991dcb1ae434ffba832c0ad50b890afac7311111"
        assert ani_log["insertions"] == 3
        assert ani_log["deletions"] == 1

    def test_populate_files(self, log_ctrl_model):
        """Test populating files in student direcotory.

        :note: Using fake stuff because this function just a bridge to
            model and didn't do anything important. the correspond logic
            model already tested in test_model.
        """
        log_ctrl, log_model = log_ctrl_model
        log_model.read_files = cf.fake_read_files

        files = log_ctrl.populate_files()
        assert files[0] == "tugas-tif.txt"

    def test_populate_auth_info(self, log_ctrl_model):
        """Test populating auth info in certain commit.
        :note: it's just a bridge function.
        """
        log_ctrl, log_model = log_ctrl_model
        log_model.read_auth_info = cf.fake_read_auth_info

        sha = "991dcb1ae434ffba832c0ad50b890afac7310608"
        auth_info = log_ctrl.populate_auth_info(sha)
        assert auth_info == ["ani", "ani-machine", "111.111.111"]

    def test_populate_all_windows(self, log_ctrl_model):
        """Test populating auth info in certain commit.

        :note: it's just a bridge function.
        """
        log_ctrl, log_model = log_ctrl_model
        log_model.read_all_windows = cf.fake_read_all_windows

        sha = "991dcb1ae434ffba832c0ad50b890afac7310608"
        all_windows = log_ctrl.populate_all_windows(sha)
        assert all_windows == [
            "emacs@screencast",
            "FrontPage - Python Wiki - Firefox Developer Edition",
            "bash",
        ]

    def test_populate_focused_window(self, log_ctrl_model):
        """Test populating focused in certain commit.

        :note: it's just a bridge function.
        """
        log_ctrl, log_model = log_ctrl_model
        log_model.read_focused_window = cf.fake_read_focused_window

        sha = "991dcb1ae434ffba832c0ad50b890afac7310608"
        focused_window = log_ctrl.populate_focused_window(sha)
        assert focused_window == "bash"

    def test_take_diff_body(self, log_ctrl):
        """Test taking diff body using dummy data."""
        ani_diff = fixture("ani_diff").decode()
        body = log_ctrl.take_diff_body(ani_diff)

        body_real = " ani 1\n+ani 2"
        assert body == body_real

    def test_wrap_with_html(self, log_ctrl):
        """Test wrapping diff body with html using dummy data."""
        diff = "- ani 1\n+ani 2"
        colored_diff = log_ctrl.wrap_with_html(diff)

        colored_diff_real = fixture("colored_diff").decode()
        assert colored_diff == colored_diff_real

    def test_get_diff(self, log_ctrl_model):
        """Test getting diff in certain commit.

        :note: it's just a bridge function.
        """
        log_ctrl, log_model = log_ctrl_model
        log_model.read_diff = cf.fake_read_diff
        log_model.take_diff_body = cf.fake_take_diff_body
        log_model.wrap_with_html = cf.fake_wrap_with_html

        sha = "991dcb1ae434ffba832c0ad50b890afac7310608"
        file_content = log_ctrl.get_diff("tugas-tif.txt", sha)
        file_content_real = (
            " ani 1<br/><span style='color:green;white-space:pre;'>+ani 2</span>"
        )
        assert file_content == file_content_real

    def test_populate_file_content(self, log_ctrl_model):
        """Test populating file content

        :note: it's just a bridge function.
        """
        log_ctrl, log_model = log_ctrl_model
        log_model.is_exists = cf.fake_is_exists
        log_model.read_file = cf.fake_read_file
        log_ctrl.get_diff = cf.fake_get_diff

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
