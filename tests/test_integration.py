import pytest
import os.path as osp

from Lupv.models.main import MainModel
from Lupv.controllers.main import MainController
from Lupv.models.logs import LogModel
from Lupv.controllers.log import LogController
from tests.helper import fixture
from tests.fixtures import record_fixture
from tests.fakes import controller_fake as cf


class TestIntegration:
    @pytest.fixture
    def log_ctrl_model(self):
        """LogController fixture.
        Create LogController instance and disconnect all signal.
        """
        main_model = MainModel()
        # main_model.record_path_changed.disconnect(main_model.read_students_records)

        log_model = LogModel(main_model)
        # log_model.current_student_dir_changed.disconnect(
        #     log_model.on_current_student_dir_changed
        # )

        main_ctrl = MainController(main_model)
        log_ctrl = LogController(main_ctrl, log_model)

        record_path = osp.join(osp.dirname(__file__), "student_tasks")
        student_path = osp.join(record_path, "ani-1111")
        log_model.record_path = record_path
        log_model.current_student_dir = "ani-1111"  # use ani only for this test
        log_model.student_path = student_path
        log_model.on_current_student_dir_changed()

        return log_ctrl, log_model

    def test_populate_logs_no_records(self, log_ctrl_model):
        """Test populating student logs using dummy data."""
        log_ctrl, log_model = log_ctrl_model
        log_model.student_records = []

        ani_logs = list(log_ctrl.populate_logs())

        assert ani_logs == []

    def test_populate_logs_no_file(self, log_ctrl_model):
        """Test populating student logs using dummy data."""
        log_ctrl, log_model = log_ctrl_model

        ani_logs = list(log_ctrl.populate_logs(selected_file=None))

        ani_log = ani_logs[0]
        assert "ago" in ani_log["relative_time"]
        assert ani_log["time"] == "Tue, 26 Mar 2019, 13:52:48"
        assert ani_log["sha"] == "991dcb1ae434ffba832c0ad50b890afac7310608"
        assert ani_log["insertions"] == 0
        assert ani_log["deletions"] == 0

    def test_populate_logs(self, log_ctrl_model):
        """Test populating student logs using dummy data."""
        log_ctrl, log_model = log_ctrl_model

        ani_logs = list(log_ctrl.populate_logs(selected_file="tugas-none.txt"))

        ani_log = ani_logs[0]
        assert "ago" in ani_log["relative_time"]
        assert ani_log["time"] == "Tue, 26 Mar 2019, 13:52:48"
        assert ani_log["sha"] == "991dcb1ae434ffba832c0ad50b890afac7310608"
        assert ani_log["insertions"] == 0
        assert ani_log["deletions"] == 0

    def test_populate_logs(self, log_ctrl_model):
        """Test populating student logs using dummy data."""
        log_ctrl, log_model = log_ctrl_model

        ani_logs = list(log_ctrl.populate_logs(selected_file="tugas-tif.txt"))

        ani_log = ani_logs[0]
        assert "ago" in ani_log["relative_time"]
        assert ani_log["time"] == "Tue, 26 Mar 2019, 13:52:48"
        assert ani_log["sha"] == "991dcb1ae434ffba832c0ad50b890afac7310608"
        assert ani_log["insertions"] == 1
        assert ani_log["deletions"] == 0
