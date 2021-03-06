import pytest
import os.path as osp
from Lupv.models.main import MainModel
from Lupv.models.logs import LogModel
from Lupv.models.search import SearchModel
from tests.helper import fixture
from tests.fakes import model_fake as mf


class TestMainModel:
    @pytest.fixture
    def main_model(self):
        """MainModel fixture.
        Create MainModel instance and disconnect all signal.
        """
        main_model = MainModel()
        main_model.record_path_changed.disconnect(main_model.read_students_records)
        return main_model

    def test_property(self, main_model):
        """Test MainModel property with dummy value."""
        main_model.record_path = "/some/path"
        main_model.students_records = "Record"

        assert main_model.record_path == "/some/path"
        assert main_model.students_records == "Record"

    def test_get_student_dirs(self, main_model):
        """Test get_student_dirs with dummy directories."""
        record_path = osp.join(osp.dirname(__file__), "student_tasks")
        main_model.record_path = record_path

        student_dirs = main_model.get_student_dirs()

        assert set(["budi-2222", "ani-1111"]).issubset(student_dirs)

    def test_get_records(self, main_model):
        """Test get_records with real git objects."""
        record_path = osp.join(osp.dirname(__file__), "student_tasks")
        ani_path = osp.join(record_path, "ani-1111")
        budi_path = osp.join(record_path, "budi-2222")
        ani_records = main_model.get_records(ani_path)
        budi_records = main_model.get_records(budi_path)

        assert len(ani_records) == 4
        assert len(budi_records) == 5

    def test_read_student_records(self, main_model):
        """Test reading students records using fake commit from this repo and
        dummy student directories.
        """
        main_model.get_student_dirs = mf.fake_student_dirs
        main_model.get_records = mf.fake_get_records

        main_model.read_students_records()
        ani_record = main_model.students_records[0]
        budi_record = main_model.students_records[1]

        assert ani_record["name"] == "ani"
        assert ani_record["student_id"] == "1111"
        assert len(ani_record["records"]) == 3
        assert budi_record["name"] == "budi"
        assert budi_record["student_id"] == "2222"
        assert len(budi_record["records"]) == 3


class TestLogModel:
    @pytest.fixture
    def log_model(self):
        """LogModel fixture.
        Create LogModel instance and disconnect all signal.
        """
        main_model = MainModel()
        log_model = LogModel(main_model)
        log_model.current_student_dir_changed.disconnect(
            log_model.on_current_student_dir_changed
        )
        return log_model

    @pytest.fixture
    def student_paths(self):
        """Construct student path.

        :returns: real student_path for ani and budi in /test/student_tasks/
        """
        record_path = osp.join(osp.dirname(__file__), "student_tasks")
        ani_path = osp.join(record_path, "ani-1111")
        budi_path = osp.join(record_path, "budi-2222")
        return ani_path, budi_path

    def test_property(self, log_model):
        """Test LogModel properties."""
        log_model.record_path = "home/x/test"
        log_model.student_path = "home/x/test/ani"
        log_model.current_student_dir = "ani-1111"
        log_model.student_records = None
        log_model.student_repo = None

        assert log_model.record_path == "home/x/test"
        assert log_model.student_path == "home/x/test/ani"
        assert log_model.current_student_dir == "ani-1111"
        assert log_model.student_records is None
        assert log_model.student_repo is None

    def test_read_files(self, log_model, student_paths):
        """Test finding files in student directory with dummy data."""
        ani_path, budi_path = student_paths
        log_model.student_path = ani_path
        files = log_model.read_files()

        assert files == ["tugas-tif.txt"]

    def test_read_focused_window(self, log_model, student_paths):
        """Test reading focused window in specific commit with real data."""
        ani_path, budi_path = student_paths
        # check if it can cycle multiple students
        log_model.student_repo = mf.fake_student_repo(ani_path)
        ani_focused_window = log_model.read_focused_window(
            "243ea13b1248bd2ebf4cd3ad550816619e08b470"
        )
        log_model.student_repo = mf.fake_student_repo(budi_path)
        budi_focused_window = log_model.read_focused_window(
            "961e5cc0f1fb780e554beb8a5b48f26f586b89d1"
        )

        assert ani_focused_window == "bash"
        assert budi_focused_window == "~/TESTS/budi-2222/tugas-tif.txt"

    def test_read_auth_info(self, log_model, student_paths):
        """Test reading auth info in specific commit with real data."""
        ani_path, budi_path = student_paths
        log_model.student_repo = mf.fake_student_repo(ani_path)
        ani_auth_info = log_model.read_auth_info(
            "243ea13b1248bd2ebf4cd3ad550816619e08b470"
        )
        log_model.student_repo = mf.fake_student_repo(budi_path)
        budi_auth_info = log_model.read_auth_info(
            "325b2dae6ab4e56a22ff5fc457e5ccff72740cfd"
        )

        assert ani_auth_info == ["ani", "ani-machine", "111.111.111"]
        assert budi_auth_info == ["budi", "budi-machine", "22.2.2222"]

    def test_read_all_windows(self, log_model, student_paths):
        """Test reading all windows in specific commit with real data."""
        ani_path, budi_path = student_paths
        log_model.student_repo = mf.fake_student_repo(ani_path)
        ani_auth_info = log_model.read_all_windows(
            "e356b905c53c683818f5dacc2f880e3fd7e88d3c"
        )
        log_model.student_repo = mf.fake_student_repo(budi_path)
        budi_auth_info = log_model.read_all_windows(
            "325b2dae6ab4e56a22ff5fc457e5ccff72740cfd"
        )

        assert ani_auth_info == [
            "~/TESTS/ani-1111/tugas-tif.txt",
            "FrontPage - Python Wiki - Firefox Developer Edition",
            "bash",
        ]
        assert budi_auth_info == [
            "emacs@screencast",
            "FrontPage - Python Wiki - Firefox Developer Edition",
            "bash",
        ]

    def test_read_file(self, log_model, student_paths):
        """Test reading file content in specific commit with real data."""
        ani_path, budi_path = student_paths
        log_model.student_repo = mf.fake_student_repo(ani_path)
        filename = "tugas-tif.txt"
        ani_file = log_model.read_file(
            filename, "991dcb1ae434ffba832c0ad50b890afac7310608"
        )
        log_model.student_repo = mf.fake_student_repo(budi_path)
        budi_file = log_model.read_file(
            filename, "422b64b3811192f412d223fcd5455a661aac0dbf"
        )

        assert ani_file == "ani 1\nani 2"
        assert budi_file == "budi line 1\nbudi line 2"

    def test_read_diff(self, log_model, student_paths):
        """Test reading diff in specific commit with real data."""
        ani_path, budi_path = student_paths
        log_model.student_repo = mf.fake_student_repo(ani_path)
        filename = "tugas-tif.txt"
        ani_diff = log_model.read_diff(
            filename, "991dcb1ae434ffba832c0ad50b890afac7310608"
        )
        log_model.student_repo = mf.fake_student_repo(budi_path)
        budi_diff = log_model.read_diff(
            filename, "422b64b3811192f412d223fcd5455a661aac0dbf"
        )

        ani_diff_real = fixture("ani_diff").decode()
        budi_diff_real = fixture("budi_diff").decode()
        assert ani_diff == ani_diff_real
        assert budi_diff == budi_diff_real

    def test_is_exists(self, log_model, student_paths):
        """Test checking if certain file exists in specific commit with real data."""
        ani_path, budi_path = student_paths
        log_model.student_repo = mf.fake_student_repo(ani_path)
        filename = "tugas-tif.txt"
        ani_exists = log_model.is_exists(
            filename, "991dcb1ae434ffba832c0ad50b890afac7310608"
        )
        log_model.student_repo = mf.fake_student_repo(budi_path)
        budi_exists = log_model.is_exists(
            filename, "422b64b3811192f412d223fcd5455a661aac0dbf"
        )

        assert ani_exists is True
        assert budi_exists is True

    def test_on_current_student_dir_changed(self, log_model, student_paths):
        """Test some action that runs automatically when student_dir changed."""
        record_path = osp.join(osp.dirname(__file__), "student_tasks")
        log_model.record_path = record_path
        log_model.current_student_dir = "ani-1111"
        log_model.on_current_student_dir_changed()

        assert len(log_model.student_records) == 4


class TestSearchModel:
    @pytest.fixture
    def search_model(self):
        """SearchModel fixture."""
        main_model = MainModel()
        search_model = SearchModel(main_model)
        return search_model

    def test_property(self, search_model):
        """Test SearchModel properties."""
        search_model.prev_editdistances = None
        assert search_model.prev_editdistances is None

    def test_read_sample_files(self):
        """Test finding files from one sample student with real data."""
        main_model = MainModel()
        search_model = SearchModel(main_model)

        record_path = osp.join(osp.dirname(__file__), "student_tasks")
        main_model.record_path = record_path
        files = search_model.read_sample_files()

        assert files == ["tugas-tif.txt"]

    def test_read_editdistances(self, search_model):
        """Test reading exported editdistances file with real data."""
        ed_path = osp.join(
            osp.dirname(__file__),
            "student_tasks",
            "lupv-notes",
            "tugas-tif.txt-editdistance.lup",
        )
        ed = search_model.read_editdistances(ed_path)

        assert "ani-1111" in list(ed.keys())
        assert "budi-2222" in list(ed.keys())

    def test_write_editdistances(self, search_model, tmpdir):
        """Test writing editdistance to dummy file with dummy data."""
        ed_dummy = {"ani-1111": {"task-name": "tugas-tif.txt"}}
        ed_path = tmpdir.join("editdistance-exported.lup")
        search_model.write_editdistances(ed_dummy, ed_path)
        ed = search_model.read_editdistances(ed_path)
        assert "ani-1111" in list(ed.keys())
