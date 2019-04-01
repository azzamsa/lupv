import pytest
import sys
import os.path as osp

from PyQt5.QtWidgets import QApplication

from Lupv.models.main import MainModel
from Lupv.controllers.main import MainController
from Lupv.views.main import MainView
from tests.fakes import controller_fake as cf
from tests.fakes import view_fake as vf


class Lupv(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.main_model = MainModel()
        self.main_ctrl = MainController(self.main_model)
        self.main_view = MainView(self.main_ctrl, self.main_model)


class TestMainView:
    @pytest.fixture
    def lupv(self):
        lupv = Lupv(sys.argv)
        lupv.main_view._search_view.plt.close("all")
        return lupv

    def test_toggle_spinner(self, lupv):
        """Test toggling spinner progress bar."""
        lupv.main_view.toggle_spinner("work")
        spinner_work_idx = lupv.main_view._ui.spinner_stack.currentIndex()

        lupv.main_view.toggle_spinner("ready")
        spinner_ready_idx = lupv.main_view._ui.spinner_stack.currentIndex()

        assert spinner_work_idx == 1
        assert spinner_ready_idx == 0

    def test_display_records(self, lupv):
        """Test displaying record to `main_table`."""
        lupv.main_ctrl.populate_students_records = cf.fake_populate_students_records
        lupv.main_view.display_records()
        main_table = lupv.main_view._ui.main_table
        first_colum = main_table.item(0, 0).text()
        second_colum = main_table.item(0, 1).text()

        assert set([first_colum]).issubset(["budi", "ani"])
        assert set([second_colum]).issubset(["1111", "2222"])

    def test_change_table_appearance(self, lupv):
        """Test changing table appearance."""
        lupv.main_ctrl.populate_students_records = cf.fake_populate_students_records
        main_table = lupv.main_view._ui.main_table

        lupv.main_view.display_records()
        before_change = main_table.isColumnHidden(4)

        lupv.main_view.change_table_appearance("real")
        after_change = main_table.isColumnHidden(4)

        assert before_change is True
        assert after_change is False

    def test_toggle_main_widgets(self, lupv):
        """Test toggling widget visibility/enable-ity."""
        before_change = lupv.main_view._ui.export_editdistance_action.isEnabled()
        lupv.main_view.toggle_main_widgets()
        after_change = lupv.main_view._ui.export_editdistance_action.isEnabled()

        assert before_change is False
        assert after_change is True

    def test_get_selected_student(self, lupv):
        """Test getting selected students record.

        :note: currentRow faked because no UI interaction involved.
        """
        lupv.main_ctrl.populate_students_records = cf.fake_populate_students_records
        main_table = lupv.main_view._ui.main_table
        main_table.currentRow = vf.fake_currentRow

        lupv.main_view.display_records()
        selected_student_dir = lupv.main_view.get_selected_student()

        assert set([selected_student_dir]).issubset(["budi-2222", "ani-1111"])

    def test_show_log_view(self, lupv):
        """Test showing `log_view`."""
        lupv.main_view.get_selected_student = vf.fake_get_selected_student
        lupv.main_ctrl.change_current_student_dir = vf.fake_function
        lupv.main_view._log_view.display_logs = vf.fake_function
        lupv.main_view._log_view.display_filename = vf.fake_function
        record_path = osp.join(osp.dirname(__file__), "student_tasks")
        lupv.main_view._main_ctrl.change_record_path(record_path)

        stack_idx_before = lupv.main_view._ui.stackedWidget.currentIndex()
        lupv.main_view.show_log_view()
        stack_idx_after = lupv.main_view._ui.stackedWidget.currentIndex()

        assert stack_idx_before == 0
        assert stack_idx_after == 1
