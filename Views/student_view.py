from Model.logs import Logs
from Views.student_window import Ui_Form

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem


class StudentView(QWidget, Ui_Form):

    def __init__(self, model, controller, student_dir):
        super().__init__()
        self.setupUi(self)
        self._student_dir = student_dir
        self._model = model
        self._controller = controller

        self.name_label.setText(student_dir)
        self.setWindowTitle(student_dir)

        self.push_me.clicked.connect(self.populate_log)

    def parse_logs(self):
        record_path = self._model.get_record_path()
        student_dir = record_path + '/' + self._student_dir
        recs = self._controller.get_records(student_dir)
        logs = []

        for rec in recs:
            name = rec.committer.name
            summary = rec.summary
            email = rec.committer.email
            log = Logs(name, summary, email)
            logs.append(log)

        return logs

    def populate_log(self):
        logs = self.parse_logs()
        for l in logs:
            QTreeWidgetItem(self.log_tree,
                            [str(l.name),
                             str(l.email),
                             str(l.summary)])
