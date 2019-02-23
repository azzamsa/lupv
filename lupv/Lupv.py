import sys

from PyQt5.QtWidgets import QApplication

from Controllers.controller import Controller
from Views.main_view import MainView


class Lupv(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.controller = Controller()
        self.main_view = MainView(self.controller)


if __name__ == "__main__":
    lupv = Lupv(sys.argv)

    sys.exit(lupv.exec_())
