from os.path import join
from collections import defaultdict
import yaml

from PyQt5.QtCore import QObject

from Model.search import Suspects
from Model.search import IpGroup
from Model.search import StudentWindow
from Model.search import StudentEditDistance


class SearchController(QObject):
    def __init__(self, record_path, controller):
        super().__init__()
        self._record_path = record_path
        self._controller = controller

    def get_student_info(self, student_dir, datetime=None):
        date = None
        name, student_id = [str(student_dir).split("-")[x] for x in [0, 1]]
        if datetime:
            date = "{:%a, %d %b %Y, %H:%M:%S}".format(datetime)
        return name, student_id, date

    def get_sample_files(self):
        students = self._controller.get_student_dirs(self._record_path)
        student_sample_path = join(self._record_path, students[0])
        files = self._controller.get_files(student_sample_path)
        return files

    def records_iterator(self):
        student_dirs = self._controller.get_student_dirs(self._record_path)
        for student in student_dirs:
            student_path = join(self._record_path, student)
            student_repo = self._controller.initialize_repo(student_path)
            records = self._controller.get_records(student_path)

            for rec in records:
                yield student, student_repo, rec

    def construct_2level(self, suspects):
        suspect_parentchild = defaultdict(list)
        for suspect in suspects:
            key = "{}-{}".format(suspect.name, suspect.student_id)
            suspect_parentchild[key].append(suspect)
        return suspect_parentchild

    def get_suspects(self, insertions_limit, filename):
        suspects = []

        for student, student_repo, rec in self.records_iterator():
            if self._controller.is_exists(filename, rec.hexsha, student_repo):
                insertions = rec.stats.files[filename]["insertions"]
                if insertions > insertions_limit:
                    name, student_id, date = self.get_student_info(
                        student, rec.committed_datetime
                    )

                    suspect = Suspects(name, student_id, filename, insertions, date)
                    suspects.append(suspect)

        suspects_parentchild = self.construct_2level(suspects)
        return suspects_parentchild

    def group_by_ip(self, ip_group_2level):
        # construct ip : students
        student_group = defaultdict(list)
        for student in ip_group_2level:
            ip = "{}".format(student.ip)
            student_group[ip].append(student)

        ip_group_3level = {}
        # construct ip : student : students
        for key in student_group.keys():
            models = student_group[key]
            student_students = defaultdict(list)
            for model in models:
                student_key = "{}-{}".format(model.name, model.student_id)
                student_students[student_key].append(model)
            ip_group_3level[key] = student_students
        return ip_group_3level

    def read_ips(self):
        ip_group_2level = []

        for student, student_repo, rec in self.records_iterator():
            auth_file = self._controller.read_auth_info(rec.hexsha, student_repo)
            ip = auth_file[2]
            name, student_id, date = self.get_student_info(
                student, rec.committed_datetime
            )

            ip_group = IpGroup(ip, name, student_id, date)
            ip_group_2level.append(ip_group)

        ip_groups_3level = self.group_by_ip(ip_group_2level)
        return ip_groups_3level

    def idx_of_substring(self, mylist, substring):
        for idx, string in enumerate(mylist):
            if substring in string:
                return idx

    def read_windows(self, search_key):
        student_window = None

        for student, student_repo, rec in self.records_iterator():
            windows = self._controller.read_all_windows(rec.hexsha, student_repo)
            windows_lower = [item.lower() for item in windows]

            found = self.idx_of_substring(windows_lower, search_key)
            if found:
                window_name = windows[found]
                student_name, student_id, date = self.get_student_info(
                    student, rec.committed_datetime
                )

                student_window = StudentWindow(
                    window_name, student_name, student_id, date
                )
                yield student_window

    def read_all_editdistance(self, filename):
        for student, student_repo, _ in self.records_iterator():
            student_path = join(self._record_path, student)
            student_repo = self._controller.initialize_repo(student_path)
            records = self._controller.get_records(student_path)

            editdistances_ax = []
            records_ax = []
            if filename:
                editdistances_ax, records_ax = self._controller.calc_editdistances(
                    filename, records, student_repo
                )

            name, student_id, _ = self.get_student_info(student)
            student_ed = StudentEditDistance(
                name, student_id, editdistances_ax, records_ax, filename
            )
            yield student_ed

    def construct_editdistance_path(self, task_name):
        editdistance_file_path = join(
            self._record_path, "lupv-notes", task_name + "-editdistance.lup"
        )
        return editdistance_file_path

    def construct_ed_graph_path(self, cur_student_name, prev_student_name):
        graph_path = join(
            self._record_path,
            "lupv-notes",
            "{}_{}.png".format(cur_student_name, prev_student_name),
        )
        return graph_path

    def export_editdistance(self, students, save_path):
        students_ed = {}
        for student in students:
            student_key = "{}-{}".format(student.name, student.student_id)
            students_ed[student_key] = dict(
                editdistances_ax=list(student.editdistances_ax),
                records_ax=list(student.records_ax),
                task_name=student.task_name,
            )

        with open(save_path, "w") as outfile:
            yaml.dump(students_ed, outfile)

    def read_editdistance_file(self, filename):
        with open(filename, "r") as infile:
            student_ed = yaml.safe_load(infile)
        return student_ed

    def get_editdistance_values(self, selected_file):
        records = self.get_student_records()
        editdistances_ax, records_ax = self._controller.calc_editdistance(
            selected_file, records, self.get_student_repo()
        )
        return editdistances_ax, records_ax
