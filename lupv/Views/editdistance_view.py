import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as
                                                FigureCanvas)
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as
                                                NavigationToolbar)
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout)


class EditDistanceView(QWidget):
    def __init__(self, editdistance_ax, student_dir):
        super().__init__()
        self._editdistance_ax = editdistance_ax
        self._student_dir = student_dir

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, self)
        self.close_btn = QPushButton('OK')
        self.close_btn.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.close_btn)
        self.setLayout(layout)

        self.draw_editdistance()

    def draw_editdistance(self):
        self.figure.clear()

        ax = self.figure.add_subplot(111)
        records_ax = self._editdistance_ax[0]
        editdistance_ax = self._editdistance_ax[1]
        random_color = (random.uniform(0, 1), random.uniform(0, 1),
                        random.uniform(0, 1))
        ax.plot(records_ax, editdistance_ax, color=random_color)

        name = self._student_dir.split('-')[0]
        nim = self._student_dir.split('-')[1]
        plt.title('{} {}'.format(name, nim))
        plt.xlabel('Records count')
        plt.ylabel('Edit distance from final sumbission')

        self.canvas.draw()
