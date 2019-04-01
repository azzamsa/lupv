import pytest
import sys

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


class TestLogView:
    @pytest.fixture
    def lupv(self):
        lupv = Lupv(sys.argv)
        return lupv

    def test_toggle_spinner(self, lupv):
        """Test toggling spinner progress bar."""
        lupv.main_view._log_view.toggle_spinner("work")
        spinner_work_idx = lupv.main_view._ui.spinner_stack.currentIndex()

        lupv.main_view._log_view.toggle_spinner("ready")
        spinner_ready_idx = lupv.main_view._ui.spinner_stack.currentIndex()

        assert spinner_work_idx == 1
        assert spinner_ready_idx == 0

    def test_get_selected_sha(self, lupv):
        """Test getting selected SHA."""
        lupv.main_view._ui.log_tree.selectedItems = vf.fake_selectedItems
        sha = lupv.main_view._log_view.get_selected_sha()
        assert sha == "dummy91dcb1ae"

    def test_display_log(self, lupv):
        """Test displaying student log."""
        log_view = lupv.main_view._log_view

        log_view.get_selected_file = vf.fake_get_selected_file
        log_view._log_ctrl.populate_logs = cf.fake_populate_logs

        log_view.display_logs()
        insertions_col_before = lupv.main_view._ui.log_tree.topLevelItem(0).text(3)

        log_view.display_logs(complete=True)
        insertions_col_after = lupv.main_view._ui.log_tree.topLevelItem(0).text(3)

        assert not insertions_col_before
        assert insertions_col_after == "3 Lines"

    def test_display_file_content(self, lupv):
        """Test displaying file content."""
        log_view = lupv.main_view._log_view

        log_view.get_selected_file = vf.fake_get_selected_file
        log_view._log_ctrl.populate_file_content = cf.fake_populate_file_content

        log_view.display_file_content("dummy91dcb1ae")
        file_content = lupv.main_view._ui.file_content_widget.toPlainText()
        assert file_content == "dummy content"

    def test_file_content_no_content(self, lupv):
        """Test displaying file content if file has no content."""
        log_view = lupv.main_view._log_view

        log_view.get_selected_file = vf.fake_get_selected_file
        log_view._log_ctrl.populate_file_content = (
            cf.fake_populate_file_content_no_content
        )

        log_view.display_file_content("dummy91dcb1ae")
        file_content = lupv.main_view._ui.file_content_widget.toPlainText()
        assert (
            file_content == 'No availibale record for "dummy_file.txt" in this period'
        )

    def test_file_content_no_selected_file(self, lupv):
        """Test displaying file content if user didn't select filename."""
        log_view = lupv.main_view._log_view

        # log_view.get_selected_file = vf.fake_get_selected_file
        log_view._log_ctrl.populate_file_content = cf.fake_populate_file_content

        log_view.display_file_content("dummy91dcb1ae")
        file_content = lupv.main_view._ui.file_content_widget.toPlainText()
        assert file_content == "No file selected, Please select one"

    def test_file_content_mode(self, lupv):
        """Test displaying file content according to selected mode."""
        log_view = lupv.main_view._log_view

        log_view.get_selected_file = vf.fake_get_selected_file
        log_view._log_ctrl.populate_file_content = cf.fake_populate_file_content

        lupv.main_view._ui.diff_mode_rbtn.setChecked(True)  # diff mode
        log_view.display_file_content("dummy91dcb1ae")
        file_content_diff = lupv.main_view._ui.file_content_widget.toPlainText()

        lupv.main_view._ui.diff_mode_rbtn.setChecked(False)  # show mode
        log_view.display_file_content("dummy91dcb1ae")
        file_content_show = lupv.main_view._ui.file_content_widget.toPlainText()

        assert file_content_diff == "dummy content"
        assert file_content_show == "dummy content"

    def test_display_filenames(self, lupv):
        """Test displaying filenames."""
        log_view = lupv.main_view._log_view
        filename_combo = lupv.main_view._ui.filename_combo

        log_view._log_ctrl.populate_files = cf.fake_populate_files

        log_view.display_filename()
        items = [filename_combo.itemText(i) for i in range(filename_combo.count())]
        assert items == ["No File Selected", "dummy.txt", "dummy_2.txt"]

    def test_get_seleted_file(self, lupv):
        """Test getting selected file."""
        log_view = lupv.main_view._log_view
        filename_combo = lupv.main_view._ui.filename_combo

        filename_combo.currentText = vf.fake_currentText

        selected_file = log_view.get_selected_file()
        assert selected_file == "selected dummy"

    def test_display_windows(self, lupv):
        """Test displaying windows name."""
        log_view = lupv.main_view._log_view
        windows_tree = lupv.main_view._ui.windows_tree

        log_view._log_ctrl.populate_focused_window = cf.fake_read_focused_window
        log_view._log_ctrl.populate_all_windows = cf.fake_read_all_windows

        log_view.display_windows("dummy91dcb1ae")
        focused_window = windows_tree.topLevelItem(0).text(0)
        all_windows = [windows_tree.topLevelItem(num).text(0) for num in [1, 2]]
        all_windows_real = [
            "emacs@screencast",
            "FrontPage - Python Wiki - Firefox Developer Edition",
        ]
        assert focused_window == "bash"
        assert set(all_windows).issubset(all_windows_real)

    def test_display_auth_info(self, lupv):
        """Test displaying student auth information."""
        log_view = lupv.main_view._log_view

        log_view._log_ctrl.populate_auth_info = cf.fake_read_auth_info

        log_view.display_auth_info("dummy91dcb1ae")
        name = lupv.main_view._ui.name_lbl.text()
        machine = lupv.main_view._ui.machine_lbl.text()
        ip = lupv.main_view._ui.ip_lbl.text()
        assert name == "ani"
        assert machine == "ani-machine"
        assert ip == "111.111.111"

    def test_log_appearance_changed(self, lupv):
        """Test toggling appearance."""
        log_view = lupv.main_view._log_view

        log_view.get_selected_file = vf.fake_get_selected_file
        log_view._log_ctrl.populate_logs = cf.fake_populate_logs

        log_view.display_logs()

        date_col_before = lupv.main_view._ui.log_tree.isColumnHidden(1)
        log_view.log_appearance_changed("dateformat")
        date_col_after = lupv.main_view._ui.log_tree.isColumnHidden(1)

        assert date_col_before is False
        assert date_col_after is True

    def test_log_appearance_changed_stats(self, lupv):
        """Test toggling stats appearance."""
        log_view = lupv.main_view._log_view

        log_view.get_selected_file = vf.fake_get_selected_file
        log_view._log_ctrl.populate_logs = cf.fake_populate_logs

        log_view.display_logs()

        date_col_before = lupv.main_view._ui.log_tree.isColumnHidden(3)
        log_view.log_appearance_changed("stats")
        date_col_after = lupv.main_view._ui.log_tree.isColumnHidden(3)

        assert date_col_before is False
        assert date_col_after is True

    def test_log_appearance_changed_stats_checked(self, lupv):
        """Test toggling stats appearance."""
        log_view = lupv.main_view._log_view

        log_view.get_selected_file = vf.fake_get_selected_file
        log_view._log_ctrl.populate_logs = cf.fake_populate_logs

        log_view.display_logs()

        date_col_before = lupv.main_view._ui.log_tree.isColumnHidden(3)
        lupv.main_view._ui.stats_check.setChecked(True)
        log_view.log_appearance_changed("stats")
        date_col_after = lupv.main_view._ui.log_tree.isColumnHidden(3)

        assert date_col_before is False
        assert date_col_after is False

    def test_log_selection_changed(self, lupv):
        """Test if selection changed in log_tree."""
        log_view = lupv.main_view._log_view

        log_view.get_selected_sha = vf.fake_get_selected_sha
        log_view.display_file_content = vf.fake_function
        log_view.display_windows = vf.fake_function
        log_view.display_auth_info = vf.fake_function

        log_view.log_selection_changed()
        assert True  # all internal function has been tested
