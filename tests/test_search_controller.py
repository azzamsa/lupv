import pytest
import os.path as osp
from collections import defaultdict

from Lupv.models.main import MainModel
from Lupv.models.logs import LogModel
from Lupv.models.search import SearchModel
from Lupv.controllers.search import SearchController

from tests.fixtures import search_controller_fixture as scf
from tests.fixtures import controller_fixture as cf
from tests.fixtures import model_fixture as mf


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

    @pytest.fixture
    def search_ctrl_log_model(self):
        main_model = MainModel()
        record_path = osp.join(osp.dirname(__file__), "student_tasks")
        main_model.record_path = record_path

        log_model = LogModel(main_model)
        search_model = SearchModel(main_model)
        search_ctrl = SearchController(main_model, search_model, log_model)
        return search_ctrl, log_model

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
        students = scf.students
        group = search_ctrl.group_by_name(students)

        ani_one = group["ani-1111"][0]
        ani_two = group["ani-1111"][1]
        assert list(group.keys()) == ["budi-2222", "ani-1111"]
        assert len(group["ani-1111"]) == 2
        assert len(group["ani-1111"]) == 2
        assert ani_one["name"] == "ani"
        assert ani_two["student_id"] == "1111"

    def fake_analyze_suspects(self, insertions_limit, filename):
        return scf.students

    def fake_group_by_name(self, students):
        return "this is just bridge function"

    def test_get_suspects(self, search_ctrl):
        """:note: this is just bridge function. All logic already tested above."""
        search_ctrl.analyze_suspects = self.fake_analyze_suspects
        search_ctrl.group_by_name = self.fake_group_by_name
        grouped_suspects = search_ctrl.get_suspects(1, "tugas-tif.txt")
        assert type(grouped_suspects) is str

    def test_get_student_ips(self, search_ctrl_log_model):
        """Test getting students ip using using dummy data.
        :note: Faked function already tested before.
        """
        search_ctrl, log_model = search_ctrl_log_model
        search_ctrl.records_iterator = cf.fake_record_iterator
        log_model.read_auth_info = cf.fake_read_auth_info

        students_ip = search_ctrl.get_student_ips()

        assert students_ip[0]["ip"] == "111.111.111"
        assert students_ip[0]["name"] == "ani"
        assert students_ip[0]["student_id"] == "1111"
        assert students_ip[0]["date"] == "Sat, 30 Mar 2019, 01:00:57"

    def test_group_by_ip(self, search_ctrl):
        """Test grouping student dictionary by ip using dummy data."""
        student_ips = scf.student_ips
        group = search_ctrl.group_by_ip(student_ips)

        budi_one = group["22.2.2222"][0]
        ani_one = group["111.111.111"][0]
        assert list(group.keys()) == ["22.2.2222", "111.111.111"]
        assert budi_one["name"] == "budi"
        assert budi_one["student_id"] == "2222"
        assert ani_one["name"] == "ani"
        assert ani_one["student_id"] == "1111"

    def test_multigroup_child(self, search_ctrl):
        """Test multi level grouping student dictionary by ip using dummy data."""
        grouped_students = scf.grouped_students
        group = search_ctrl.multigroup_child(grouped_students)

        assert list(group.keys()) == ["22.2.2222", "111.111.111"]
        assert list(group["22.2.2222"].keys()) == ["budi-2222"]
        assert list(group["111.111.111"].keys()) == ["ani-1111"]

    def test_get_student_ip_groups(self, search_ctrl):
        """:note: bridge function."""
        search_ctrl.get_student_ips = cf.fake_get_student_ips
        search_ctrl.group_by_ip = cf.fake_group_by_id
        search_ctrl.multigroup_child = cf.fake_multigroup_child

        multi_group_real = scf.multigroup_students
        multi_group = search_ctrl.get_student_ip_groups()
        assert multi_group is multi_group_real

    def test_idx_of_substring(self, search_ctrl):
        """Test getting index of substring in list using dummy data."""
        windows = [
            "emacs@screencast",
            "FrontPage - Python Wiki - Firefox Developer Edition",
            "bash",
        ]
        windows_lower = [item.lower() for item in windows]
        idx = search_ctrl.idx_of_substring(windows_lower, "firefox")

        assert idx == 1

    def test_collect_student_windows(self, search_ctrl_log_model):
        """Test getting students ip using using dummy data.
        :note: Faked function already tested before.
        """
        search_ctrl, log_model = search_ctrl_log_model
        search_ctrl.records_iterator = cf.fake_record_iterator
        log_model.read_all_windows = cf.fake_read_all_windows

        student_windows = search_ctrl.collect_student_windows("firefox")

        assert list(student_windows[0].keys()) == [
            "window_name",
            "name",
            "student_id",
            "date",
        ]
        assert "Firefox" in student_windows[0]["window_name"]

    def test_get_student_windows(self, search_ctrl_log_model):
        """:note: bridge function."""
        search_ctrl, log_model = search_ctrl_log_model
        search_ctrl.collect_student_windows = cf.fake_collect_student_windows

        student_windows_group = search_ctrl.get_student_windows("firefox")

        assert list(student_windows_group.keys()) == ["ani-1111", "budi-2222"]
        assert len(student_windows_group["budi-2222"]) == 1
        assert "Firefox" in student_windows_group["budi-2222"][0]["window_name"]

    def test_populate_student_dirs(self, search_ctrl_log_model):
        """:note: bridge function."""
        main_model = MainModel()
        record_path = osp.join(osp.dirname(__file__), "student_tasks")
        main_model.record_path = record_path

        log_model = LogModel(main_model)
        search_model = SearchModel(main_model)
        search_ctrl = SearchController(main_model, search_model, log_model)

        main_model.get_student_dirs = mf.fake_student_dirs

        student_dirs = search_ctrl.populate_student_dirs()
        assert student_dirs == ["ani-1111", "budi-2222"]

    def test_load_prev_editdistances(self):
        """:note: bridge function."""
        main_model = MainModel()
        record_path = osp.join(osp.dirname(__file__), "student_tasks")
        main_model.record_path = record_path

        log_model = LogModel(main_model)
        search_model = SearchModel(main_model)
        search_ctrl = SearchController(main_model, search_model, log_model)

        search_model.read_editdistances = mf.fake_read_editdistances

        ed_path = "dummy/path"
        search_ctrl.load_prev_editdistances(ed_path)
        assert search_model.prev_editdistances is not None

    def test_get_prev_student_names(self, search_ctrl):
        """Test getting previous students name from exported editdistance using dummy data.
        :note: Faked function already tested before.
        """
        main_model = MainModel()
        record_path = osp.join(osp.dirname(__file__), "student_tasks")
        main_model.record_path = record_path

        log_model = LogModel(main_model)
        search_model = SearchModel(main_model)
        search_ctrl = SearchController(main_model, search_model, log_model)

        search_model.prev_editdistances = scf.students_ed
        prev_student_names = search_ctrl.get_prev_student_names()

        assert prev_student_names == ["budi-2222", "ani-1111"]

    def test_get_prev_filename_sample(self, search_ctrl):
        """Test getting previous filename from exported editdistance using dummy data.
        :note: Faked function already tested before.
        """
        main_model = MainModel()
        record_path = osp.join(osp.dirname(__file__), "student_tasks")
        main_model.record_path = record_path

        log_model = LogModel(main_model)
        search_model = SearchModel(main_model)
        search_ctrl = SearchController(main_model, search_model, log_model)

        search_model.prev_editdistances = scf.students_ed

        sample_filename = search_ctrl.get_prev_filename_sample()
        assert sample_filename == "tugas-tif.txt"

    def test_calc_prev_editdistances(self, search_ctrl):
        """Test calculating previous editdistance from exported editdistance using dummy data.
        :note: Faked function already tested before.
        """
        main_model = MainModel()
        record_path = osp.join(osp.dirname(__file__), "student_tasks")
        main_model.record_path = record_path

        log_model = LogModel(main_model)
        search_model = SearchModel(main_model)
        search_ctrl = SearchController(main_model, search_model, log_model)

        search_model.prev_editdistances = scf.students_ed

        prev_editdistances_ax, prev_records_ax = search_ctrl.calc_prev_editdistances(
            "ani-1111"
        )
        assert prev_editdistances_ax == [0, 12, 831, 843, 856]
        assert prev_records_ax == [1, 2, 3, 4, 5]

    def test__get_student_records(self, search_ctrl):
        """:note: bridge function"""
        main_model = MainModel()
        record_path = osp.join(osp.dirname(__file__), "student_tasks")
        main_model.record_path = record_path

        log_model = LogModel(main_model)
        search_model = SearchModel(main_model)
        search_ctrl = SearchController(main_model, search_model, log_model)

        main_model.get_records = mf.fake_fake_get_records

        records = search_ctrl._get_student_records("ani-1111")
        assert len(records) == 3
        assert records[0].hexsha == "991dcb1ae434ffba832c0ad50b890afac7311111"

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
