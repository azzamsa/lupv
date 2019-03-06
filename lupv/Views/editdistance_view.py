from os.path import join
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QStyle,
)

from standard import icons


class EditDistanceView(QWidget):
    def __init__(self, editdistance, record_path, student_dir):
        super().__init__()
        self._editdistances_ax, self._records_ax = editdistance
        self._record_path = record_path
        self._student_dir = student_dir

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        close_icon = icons.style(QStyle.SP_DialogCancelButton)
        save_icon = icons.style(QStyle.SP_DialogSaveButton)
        self.close_btn = QPushButton("Close")
        self.close_btn.setIcon(close_icon)
        self.close_btn.clicked.connect(self.close)
        self.save_btn = QPushButton("Save Graph")
        self.save_btn.setIcon(save_icon)
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
        ax.plot(self._records_ax, self._editdistances_ax)

        name, student_id = [self._student_dir.split("-")[x] for x in [0, 1]]
        plt.title("{} {}".format(name, student_id))
        plt.xlabel("Records count")
        plt.ylabel("Edit distance from final sumbission")

        self.canvas.draw()

        if savep:
            image_path = join(
                self._record_path, "lupv-notes", self._student_dir + ".png"
            )
            plt.savefig(image_path)
            QMessageBox.information(self, "", "Graph saved to {}".format(image_path))
