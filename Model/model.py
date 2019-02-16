from PyQt5.QtCore import QObject


class Model(QObject):
    def __init__(self):
        super().__init__()
        self._record_path = ''

    def get_record_path(self):
        return self._record_path

    def set_record_path(self, path):
        self._record_path = path
