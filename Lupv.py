import sys
import time
from PyQt5.QtWidgets import QApplication, QProgressBar, QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from Model.model import Model
from Controllers.main_controller import MainController
from Views.main_view import MainView


class Lupv(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.model = Model()
        self.main_controller = MainController(self.model)
        self.main_view = MainView(self.model, self.main_controller)


if __name__ == "__main__":
    lupv = Lupv(sys.argv)

    sys.exit(lupv.exec_())
