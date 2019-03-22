import os
import yaml
from os.path import join

from PyQt5.QtCore import QObject


class SearchModel(QObject):
    def __init__(self, main_model):
        super().__init__()
        self._prev_editdistances = None
        self._main_model = main_model

    @property
    def prev_editdistances(self):
        """Return the value of current student."""
        return self._prev_editdistances

    @prev_editdistances.setter
    def prev_editdistances(self, prev_editdistances):
        """Set the value of current student."""
        self._prev_editdistances = prev_editdistances

    def read_sample_files(self):
        """Return files in student directory."""
        record_path = self._main_model.record_path
        sample_student = self._main_model.get_student_dirs()[0]
        sample_student_path = join(record_path, sample_student)
        dirs = os.listdir(sample_student_path)
        files = []

        for item in dirs:
            if os.path.isfile(join(sample_student_path, item)):
                files.append(item)
        return files

    def read_editdistances(self, filename):
        """Read exported editdistance file."""
        with open(filename, "r") as infile:
            editdistances = yaml.safe_load(infile)
        return editdistances

    def write_editdistances(self, students_ed, save_path):
        """Write exported value to file."""
        with open(save_path, "a") as outfile:
            yaml.dump(students_ed, outfile)
