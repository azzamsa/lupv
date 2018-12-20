from PyQt5.QtCore import QObject


class Model(QObject):
    def __init__(self):
        super().__init__()
        self._record_dir = ""

    def get_record_dir(self):
        return self._record_dir

    def set_record_dir(self, record_dir):
        self._record_dir = record_dir
