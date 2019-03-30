import pytest
import os.path as osp
from datetime import datetime, timedelta
from collections import defaultdict

from Lupv.models.main import MainModel
from Lupv.controllers.main import MainController
from Lupv.models.logs import LogModel
from Lupv.controllers.log import LogController
from Lupv.models.search import SearchModel
from Lupv.controllers.search import SearchController
from tests.helper import fixture
from tests.fixtures import search_fixture
from tests.fixtures import record_fixture


class TestMainController:
    @pytest.fixture
    def main_ctrl_model(self):
        """MainController fixture.
        Create MainController instance and disconnect all signal.
        Return both main_ctrl and main_model because some function need both of them.
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
        """Test checking valid directories using real data."""
        record_path = osp.join(osp.dirname(__file__), "student_tasks")
        invalid_dirs = main_ctrl.validate(record_path)
        assert not invalid_dirs

    def test_validate_invalid_dir(self, main_ctrl, fs):
        """Test checking valid directories using real data."""
        fs.create_dir("home/x/student_tasks/ani-1111/.git")
        fs.create_dir("home/x/student_tasks/budi-2222/.git")
        fs.create_dir("home/x/student_tasks/lupv-notes")
        fs.create_dir("home/x/student_tasks/invalid-3333")

        invalid_dirs = main_ctrl.validate("home/x/student_tasks")
        assert "invalid-3333" == invalid_dirs[0]

    def test_relativize_datetime(self, main_ctrl):
        """Test convertion datetime to its relative version using dummy data."""
        # datetime.now() didn't work, must use utcnow()
        dt = datetime.utcnow() - timedelta(hours=1)
        relative_time = main_ctrl.relativize_datetime(dt)

        assert "ago" in relative_time

    def test_get_first_record_time(self, main_ctrl):
        """Test converting first.committed_datetime to human readable format
        and its relative version using dummy data."""
        dt = datetime.utcnow() - timedelta(hours=1)
        first_time, first_relative_time = main_ctrl.get_first_record_time(dt)

        current_time = "{:%a, %d %b %Y}".format(dt)
        assert current_time in first_time
        assert "ago" in first_relative_time

    def test_get_last_record_time(self, main_ctrl):
        """Test converting last.committed_datetime to human readable format
        and its relative version using dummy data."""
        dt = datetime.utcnow() - timedelta(hours=1)
        first_time, first_relative_time = main_ctrl.get_last_record_time(dt)

        current_time = "{:%a, %d %b %Y}".format(dt)
        assert current_time in first_time
        assert "ago" in first_relative_time

    def test_calc_work_duration(self, main_ctrl):
        """Test calculating delta between datetimes using dummy data."""
        first_dt = datetime.utcnow() - timedelta(hours=1)
        last_dt = datetime.utcnow() - timedelta(hours=-1)
        work_duration, work_relative_duration = main_ctrl.calc_work_duration(
            first_dt, last_dt
        )

        assert "2" in work_duration
        assert "2 hours" in work_relative_duration

    def test_populate_students_records(self, main_ctrl_model):
        """Test populating students record using real data."""
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
        assert "ago" in ani_record["first_record_relativetime"]
        assert ani_record["last_record_time"] == "Tue, 26 Mar 2019, 13:52:48"
        assert "ago" in ani_record["last_record_relativetime"]
        assert ani_record["work_duration"] == "0:00:10"
        assert ani_record["work_relative_duration"] == "10 seconds"

        assert budi_record["name"] == "budi"
        assert budi_record["student_id"] == "2222"
        assert budi_record["total_records"] == 5
        assert budi_record["first_record_time"] == "Tue, 26 Mar 2019, 14:08:18"
        assert "ago" in budi_record["first_record_relativetime"]
        assert budi_record["last_record_time"] == "Fri, 29 Mar 2019, 08:52:47"
        assert "ago" in budi_record["last_record_relativetime"]
        assert budi_record["work_duration"] == "2 days, 18:44:29"
        assert (
            budi_record["work_relative_duration"]
            == "2 days 18 hours 44 minutes 29 seconds"
        )


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
        :note: Using real data at `/test/student_tasks/ani-1111/`.
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

    def fake_read_files(self):
        return ["tugas-tif.txt"]

    def fake_read_auth_info(self, sha):
        return ["ani", "ani-machine", "111.111.111"]

    def fake_read_all_windows(self, sha):
        return [
            "emacs@screencast",
            "FrontPage - Python Wiki - Firefox Developer Edition",
            "bash",
        ]

    def fake_read_focused_window(self, sha):
        return "bash"

    def fake_read_diff(self, filename, sha):
        return fixture("ani_diff").decode()

    def fake_take_diff_body(self, diff):
        return " ani 1\n+ani 2"

    def fake_wrap_with_html(self, diff):
        return fixture("colored_diff").decode()

    def fake_is_exist(self, filename, sha):
        return True

    def fake_read_file(self, filename, sha):
        return "ani 1\nani 2"

    def fake_get_diff(self, filename, sha):
        return " ani 1<br/><span style='color:green;white-space:pre;'>+ani 2</span>"

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
        log_model.is_exists = self.fake_is_exist

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
        log_model.read_files = self.fake_read_files

        files = log_ctrl.populate_files()
        assert files[0] == "tugas-tif.txt"

    def test_populate_auth_info(self, log_ctrl_model):
        """Test populating auth info in certain commit.
        :note: it's just a bridge function.
        """
        log_ctrl, log_model = log_ctrl_model
        log_model.read_auth_info = self.fake_read_auth_info

        sha = "991dcb1ae434ffba832c0ad50b890afac7310608"
        auth_info = log_ctrl.populate_auth_info(sha)
        assert auth_info == ["ani", "ani-machine", "111.111.111"]

    def test_populate_all_windows(self, log_ctrl_model):
        """Test populating auth info in certain commit.
        :note: it's just a bridge function.
        """
        log_ctrl, log_model = log_ctrl_model
        log_model.read_all_windows = self.fake_read_all_windows

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
        log_model.read_focused_window = self.fake_read_focused_window

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
        log_model.read_diff = self.fake_read_diff
        log_model.take_diff_body = self.fake_take_diff_body
        log_model.wrap_with_html = self.fake_wrap_with_html

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
        log_model.is_exists = self.fake_is_exist
        log_model.read_file = self.fake_read_file
        log_ctrl.get_diff = self.fake_get_diff

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


class TestSearchController:
    @pytest.fixture
    def search_ctrl(self):
        """SearchController fixture."""
        main_model = MainModel()
        record_path = osp.join(osp.dirname(__file__), "student_tasks")
        main_model.record_path = record_path

        log_model = LogModel(main_model)
        search_model = SearchModel(main_model)
        search_ctrl = SearchController(main_model, search_model, log_model)
        return search_ctrl

    def test_property(self, search_ctrl):
        """Test SearchController properties."""
        search_ctrl.prev_editdistances = "foo"
        assert search_ctrl.prev_editdistances == "foo"

    def test_populate_sample_filenames(self, search_ctrl):
        """Test populating sample filename using real data."""
        files = search_ctrl.populate_sample_filenames()
        assert files[0] == "tugas-tif.txt"

    def test_student_directories_iterator(self, search_ctrl):
        """Test iterating student directories in record_path using real data."""
        directories = []
        for direcotory in search_ctrl.student_directories_iterator():
            directories.append(direcotory)

        assert directories == ["budi-2222", "ani-1111"]

    def test_record_iterator(self, search_ctrl):
        """Test iterating record of student using real data."""
        student_records = defaultdict(list)

        for student_dir, record in search_ctrl.records_iterator():
            student_records[student_dir].append(record)

        budi_last_record = student_records["budi-2222"][0]
        ani_last_record = student_records["ani-1111"][0]
        assert list(student_records.keys()) == ["budi-2222", "ani-1111"]
        assert len(student_records["budi-2222"]) == 5
        assert len(student_records["ani-1111"]) == 4
        assert budi_last_record.hexsha == "0e91ef7e3f1224f44c9174958aaaa2a6fa082f4c"
        assert ani_last_record.hexsha == "991dcb1ae434ffba832c0ad50b890afac7310608"

    def test_analyze_suspects(self, search_ctrl):
        """Test finding student that inserted more than certain line on one
        record/commit using real data.
        """
        suspects = search_ctrl.analyze_suspects(15, "tugas-tif.txt")
        suspects_real = {
            "name": "budi",
            "student_id": "2222",
            "filename": "tugas-tif.txt",
            "insertions": 19,
            "date": "Fri, 29 Mar 2019, 08:52:47",
        }
        assert suspects[0] == suspects_real

    def test_group_by_name(self, search_ctrl):
        """Test grouping student dictionary by name using dummy data."""
        students = search_fixture.students
        group = search_ctrl.group_by_name(students)

        ani_one = group["ani-1111"][0]
        ani_two = group["ani-1111"][1]
        assert list(group.keys()) == ["budi-2222", "ani-1111"]
        assert len(group["ani-1111"]) == 2
        assert len(group["ani-1111"]) == 2
        assert ani_one["name"] == "ani"
        assert ani_two["student_id"] == "1111"

    def fake_analyze_suspects(self, insertions_limit, filename):
        return search_fixture.students

    def fake_group_by_name(self, students):
        return "this is just bridge function"

    def test_get_suspects(self, search_ctrl):
        """:note: this is just bridge function. All logic already tested above."""
        search_ctrl.analyze_suspects = self.fake_analyze_suspects
        search_ctrl.group_by_name = self.fake_group_by_name
        grouped_suspects = search_ctrl.get_suspects(1, "tugas-tif.txt")
        assert type(grouped_suspects) is str

    def test_get_student_ips(self, search_ctrl):
        students_ip = search_ctrl.get_student_ips()
        student_records = defaultdict(list)
        for student_ip in students_ip:
            student_name = student_ip["name"]
            student_records[student_name].append(student_ip)

        ani_ip = student_records["ani"]
        assert ani_ip[0]["ip"] == "111.111.111"

        budi_ip = student_records["budi"]
        assert budi_ip[0]["ip"] == "22.2.2222"

    def test_group_by_ip(self, search_ctrl):
        student_ips = search_fixture.student_ips
        group = search_ctrl.group_by_ip(student_ips)

        budi_one = group["22.2.2222"][0]
        ani_one = group["111.111.111"][0]
        assert list(group.keys()) == ["22.2.2222", "111.111.111"]
        assert budi_one["name"] == "budi"
        assert budi_one["student_id"] == "2222"
        assert ani_one["name"] == "ani"
        assert ani_one["student_id"] == "1111"

    def test_multigroup_child(self, search_ctrl):
        grouped_students = search_fixture.grouped_students
        group = search_ctrl.multigroup_child(grouped_students)

        assert list(group.keys()) == ["22.2.2222", "111.111.111"]
        assert list(group["22.2.2222"].keys()) == ["budi-2222"]
        assert list(group["111.111.111"].keys()) == ["ani-1111"]

    def test_multigroup_child(self, search_ctrl):
        multi_group = search_ctrl.get_student_ip_groups()

        assert list(multi_group.keys()) == ["22.2.2222", "111.111.111"]
        assert list(multi_group["22.2.2222"].keys()) == ["budi-2222"]
        assert list(multi_group["111.111.111"].keys()) == ["ani-1111"]

    def test_idx_of_substring(self, search_ctrl):
        windows = [
            "emacs@screencast",
            "FrontPage - Python Wiki - Firefox Developer Edition",
            "bash",
        ]
        windows_lower = [item.lower() for item in windows]
        idx = search_ctrl.idx_of_substring(windows_lower, "firefox")

        assert idx == 1

    def test_collect_student_windows(self, search_ctrl):
        student_windows = search_ctrl.collect_student_windows("firefox")

        assert len(student_windows) == 8
        assert list(student_windows[0].keys()) == [
            "window_name",
            "name",
            "student_id",
            "date",
        ]
        assert "Firefox" in student_windows[0]["window_name"]

    def test_get_student_windows(self, search_ctrl):
        student_windows_group = search_ctrl.get_student_windows("firefox")

        assert list(student_windows_group.keys()) == ["budi-2222", "ani-1111"]
        assert len(student_windows_group["budi-2222"]) == 4
        assert "Firefox" in student_windows_group["budi-2222"][0]["window_name"]

    def test_populate_student_dirs(self, search_ctrl):
        student_dirs = search_ctrl.populate_student_dirs()
        assert student_dirs == ["budi-2222", "ani-1111"]

    # need search model !
    # def test_load_prev_editdistances(self, search_ctrl):
    #     ed_path = osp.join(
    #         osp.dirname(__file__),
    #         "student_tasks",
    #         "lupv-notes",
    #         "tugas-tif.txt-editdistance.lup",
    #     )
    #     search_ctrl.load_prev_editdistances(ed_path)

    def test_get_prev_student_names(self, search_ctrl):
        ed_path = osp.join(
            osp.dirname(__file__),
            "student_tasks",
            "lupv-notes",
            "tugas-tif.txt-editdistance.lup",
        )
        search_ctrl.load_prev_editdistances(ed_path)
        prev_student_names = search_ctrl.get_prev_student_names()
        assert prev_student_names == ["budi-2222", "ani-1111"]

    def test_get_prev_filename_sample(self, search_ctrl):
        ed_path = osp.join(
            osp.dirname(__file__),
            "student_tasks",
            "lupv-notes",
            "tugas-tif.txt-editdistance.lup",
        )
        search_ctrl.load_prev_editdistances(ed_path)
        sample_filename = search_ctrl.get_prev_filename_sample()
        assert sample_filename == "tugas-tif.txt"

    def test_calc_prev_editdistances(self, search_ctrl):
        ed_path = osp.join(
            osp.dirname(__file__),
            "student_tasks",
            "lupv-notes",
            "tugas-tif.txt-editdistance.lup",
        )
        search_ctrl.load_prev_editdistances(ed_path)
        prev_editdistances_ax, prev_records_ax = search_ctrl.calc_prev_editdistances(
            "ani-1111"
        )
        assert prev_editdistances_ax == [0, 12, 831, 843, 856]
        assert prev_records_ax == [1, 2, 3, 4, 5]

    def test_get_student_records(self, search_ctrl):
        records = search_ctrl._get_student_records("ani-1111")
        assert len(records) == 4
        assert records[0].hexsha == "991dcb1ae434ffba832c0ad50b890afac7310608"

    def test_calc_editdistances(self, search_ctrl):
        editdistances_ax, records_ax = search_ctrl.calc_editdistances(
            "ani-1111", "tugas-tif.txt"
        )
        assert editdistances_ax == [0, 6, 11]
        assert records_ax == [1, 2, 3]

    @pytest.fixture
    def search_ctrl_disconnect(self):
        main_model.record_path_changed.disconnect(main_model.read_students_records)
        main_model = MainModel()
        log_model = LogModel(main_model)
        log_model.current_student_dir_changed.disconnect(
            log_model.on_current_student_dir_changed
        )
        search_model = SearchModel(main_model)
        search_ctrl = SearchController(main_model, search_model, log_model)

        log_model = LogModel(main_model)
        search_model = SearchModel(main_model)
        search_ctrl = SearchController(main_model, search_model, log_model)
        return search_ctrl

    def test_create_lupvnotes_dir(self, fs):
        main_model = MainModel()
        main_model.record_path_changed.disconnect(main_model.read_students_records)
        log_model = LogModel(main_model)
        log_model.current_student_dir_changed.disconnect(
            log_model.on_current_student_dir_changed
        )
        search_model = SearchModel(main_model)
        search_ctrl = SearchController(main_model, search_model, log_model)

        log_model = LogModel(main_model)
        search_model = SearchModel(main_model)
        search_ctrl = SearchController(main_model, search_model, log_model)

        fs.create_dir("home/x/student_tasks/")

        main_model.record_path = "home/x/student_tasks"
        search_ctrl.create_lupvnotes_dir()
        assert osp.isdir("home/x/student_tasks/lupv-notes")

    def test_construct_ed_graph_path(self, search_ctrl):
        graph_path = search_ctrl.construct_ed_graph_path("ani-1111")
        assert "/lupv-notes/ani-1111.png" in graph_path

    def test_construct_editistance_path(self, search_ctrl):
        editdistance_file_path = search_ctrl.construct_editdistance_path(
            "tugas-tif2.txt"
        )
        assert "lupv-notes/tugas-tif2.txt-editdistance.lup" in editdistance_file_path

    # def test_export_editdistance(self, search_ctrl):
    #     # fs.create_dir("home/x/student_tasks/lupv-notes/")

    #     # save_path = "home/x/student_tasks/lupv-notes/tugas-tif3.txt-editdistance.lup"
    #     search_ctrl.export_editdistances('tugas-tif.txt')
    #     f = osp.exists(
    #         "home/x/student_tasks/lupv-notes//tugas-tif3.txt-editdistance.lup"
    #     )
    #     print(f)
