import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox


class EditDistanceView(QWidget):
    def __init__(self, editdistance_ax, student_ctrl, student_dir):
        super().__init__()
        self._editdistance_ax = editdistance_ax
        self._student_ctrl = student_ctrl
        self._student_dir = student_dir

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.close_btn = QPushButton("OK")
        self.close_btn.clicked.connect(self.close)
        self.save_btn = QPushButton("Save Graph")
        self.save_btn.clicked.connect(lambda: self.draw_editdistance(True))

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.close_btn)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.draw_editdistance()

    def draw_editdistance(self, savep=None):
        self.figure.clear()

        ax = self.figure.add_subplot(111)
        records_ax = self._editdistance_ax[0]
        editdistance_ax = self._editdistance_ax[1]
        random_color = (
            random.uniform(0, 1),
            random.uniform(0, 1),
            random.uniform(0, 1),
        )
        ax.plot(records_ax, editdistance_ax, color=random_color)

        name = self._student_dir.split("-")[0]
        nim = self._student_dir.split("-")[1]
        plt.title("{} {}".format(name, nim))
        plt.xlabel("Records count")
        plt.ylabel("Edit distance from final sumbission")

        self.canvas.draw()

        if savep:
            image_path = self._student_ctrl.get_student_path() + ".png"
            plt.savefig(image_path)
            QMessageBox.information(self, "", "Graph saved to {}".format(image_path))
