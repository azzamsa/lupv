import yaml
import pathlib
import editdistance as edlib
from os.path import join
from collections import defaultdict

from PyQt5.QtCore import QObject

from models.search import Suspects
from models.search import StudentIp
from models.search import StudentWindow
from models.search import StudentEditdistances


class SearchController(QObject):
    def __init__(self, main_model, search_model, log_model):
        super().__init__()
        self._main_model = main_model
        self._search_model = search_model
        self._log_model = log_model

    def get_student_info(self, student_dir, datetime=None):
        date = None
        name, student_id = [str(student_dir).split("-")[x] for x in [0, 1]]
        if datetime:
            date = "{:%a, %d %b %Y, %H:%M:%S}".format(datetime)
        return name, student_id, date

    def populate_sample_filenames(self):
        # must take random student.
        # so that it can be use even before user visiting log view
        files = self._search_model.read_sample_files()
        return files

    def records_iterator(self):
        student_dirs = self._main_model.get_student_dirs()
        record_path = self._main_model.record_path

        for student in student_dirs:
            student_path = join(record_path, student)
            records = self._main_model.get_records(student_path)

            for record in records:
                self._log_model.current_student = student
                yield student, record

    def analyze_suspects(self, insertions_limit, filename):
        suspects = []

        for student, record in self.records_iterator():
            if self._log_model.is_exists(filename, record.hexsha):
                insertions = record.stats.files[filename]["insertions"]

                if insertions > insertions_limit:
                    name, student_id, date = self.get_student_info(
                        student, record.committed_datetime
                    )

                    suspect = Suspects(name, student_id, filename, insertions, date)
                    suspects.append(suspect)

        return suspects

    def group_by_name(self, students):
        group = defaultdict(list)
        for student in students:
            key = "{}-{}".format(student.name, student.student_id)
            group[key].append(student)
        return group

    def get_suspects(self, insertions_limit, filename):
        suspects = self.analyze_suspects(insertions_limit, filename)
        grouped_suspects = self.group_by_name(suspects)
        return grouped_suspects

    # def read_ips(self):
    def get_student_ips(self):
        students_ip = []

        for student, record in self.records_iterator():
            auth_file = self._log_model.read_auth_info(record.hexsha)
            ip = auth_file[2]
            name, student_id, date = self.get_student_info(
                student, record.committed_datetime
            )

            student_ip = StudentIp(ip, name, student_id, date)
            students_ip.append(student_ip)

        # ip_groups_3level = self.group_by_ip(ip_group_2level)
        # return ip_groups_3level
        return students_ip

    # def group_by_ip(self, ip_group_2level):
    def group_by_ip(self, students):
        group = defaultdict(list)
        for student in students:
            key = "{}".format(student.ip)
            group[key].append(student)
        return group

    def multigroup_child(self, grouped_students):
        """ Create multiple level of item groups:
        1. grouped_students (accepted data):
            - 123.0
              - ani
              - ani
              - ani
            - 111.0
              - budi
        2. extract each group items to temporary holder
            - holder[key:123.0] : ani,ani,ani
        3. arrange holder items by key (or similar things)
            - ani <-- parent level
                - ani
                - ani
        4. insert step three to new dict with grandparent keys
            - 123.0 <--- grand parent
              - ani <--- parent
                - ani <--- child
                - ani
            - 111.0
              - budi
              - ani
        `grouped_by_name = defaultdict(list)` placement is crucial, because it
        will be wiped to contain new group each iteration.
        """
        group = {}

        for parent_key in grouped_students.keys():
            # extract group items by parent key
            group_temp = grouped_students[parent_key]

            grouped_by_name = defaultdict(list)
            for student in group_temp:
                # arrange group item by similar identifier
                # e.g by name
                student_name_key = "{}-{}".format(student.name, student.student_id)
                grouped_by_name[student_name_key].append(student)

            # insert grouped parent-child item to it's grandparent
            group[parent_key] = grouped_by_name

        return group

    def get_student_ip_groups(self):
        students_ip = self.get_student_ips()
        grouped_by_ip = self.group_by_ip(students_ip)
        multi_group = self.multigroup_child(grouped_by_ip)
        return multi_group

    def idx_of_substring(self, mylist, substring):
        for idx, string in enumerate(mylist):
            if substring in string:
                return idx

    def read_windows(self, search_key):
        student_window = None

        for student, record in self.records_iterator():
            windows = self._log_model.read_all_windows(record.hexsha)
            windows_lower = [item.lower() for item in windows]

            found = self.idx_of_substring(windows_lower, search_key)
            if found:
                window_name = windows[found]
                student_name, student_id, date = self.get_student_info(
                    student, record.committed_datetime
                )

                student_window = StudentWindow(
                    window_name, student_name, student_id, date
                )
                yield student_window

    #
    # Editdistance tab
    #
    def populate_student_dirs(self):
        student_dirs = self._main_model.get_student_dirs()
        return student_dirs

    def load_prev_editdistances(self, filename):
        editdistances = self._search_model.read_editdistances(filename)
        self._search_model.prev_editdistances = editdistances

    def get_prev_students(self):
        prev_editdistances = self._search_model.prev_editdistances
        prev_students = list(prev_editdistances.keys())
        return prev_students

    def get_prev_filename_sample(self):
        student_sample = self.get_prev_students()
        prev_editdistances = self._search_model.prev_editdistances
        sample_filename = prev_editdistances[student_sample[0]]["task_name"]
        return sample_filename

    def calc_prev_editdistances(self, student_name):
        editdistances = self._search_model.prev_editdistances
        prev_records_ax = editdistances[student_name]["records_ax"]
        prev_editdistances_ax = editdistances[student_name]["editdistances_ax"]
        return prev_records_ax, prev_editdistances_ax

    def _get_student_records(self, student):
        record_path = self._main_model.record_path
        student_path = join(record_path, student)
        records = self._main_model.get_records(student_path)
        return records

    def calc_editdistances(self, student, filename):
        """Calculate student's editdistance and record axis."""
        records_count = 0
        records_ax = []
        editdistances_ax = []

        records = self._get_student_records(student)
        self._log_model.current_student = student
        last_file = self._log_model.read_file(filename, records[0].hexsha)

        for record in records:
            if self._log_model.is_exists(filename, record.hexsha):
                current_file = self._log_model.read_file(filename, record.hexsha)
                editdistance_value = edlib.eval(last_file, current_file)
                editdistances_ax.append(editdistance_value)

                records_count += 1
                records_ax.append(records_count)

        return editdistances_ax, records_ax

    def create_lupvnotes_dir(self):
        """Create lupv-notes directory."""
        record_path = self._main_model.record_path
        notes_path = join(record_path, "lupv-notes")
        pathlib.Path(notes_path).mkdir(parents=True, exist_ok=True)

    def construct_ed_graph_path(self, cur_student_name, prev_student_name):
        record_path = self._main_model.record_path
        graph_path = join(
            record_path,
            "lupv-notes",
            "{}_{}.png".format(cur_student_name, prev_student_name),
        )
        return graph_path

    def calc_all_editdistance(self, filename):
        for student, _ in self.records_iterator():
            editdistances_ax, records_ax = self.calc_editdistances(student, filename)

            name, student_id, _ = self.get_student_info(student)
            student_ed = StudentEditdistances(
                name, student_id, editdistances_ax, records_ax, filename
            )
            yield student_ed

    def construct_editdistance_path(self, task_name):
        record_path = self._main_model.record_path
        editdistance_file_path = join(
            record_path, "lupv-notes", "{}-editdistance.lup".format(task_name)
        )
        return editdistance_file_path

    def export_editdistance(self, students, save_path):
        students_ed = {}
        for student in students:
            student_key = "{}-{}".format(student.name, student.student_id)
            students_ed[student_key] = dict(
                editdistances_ax=list(student.editdistances_ax),
                records_ax=list(student.records_ax),
                task_name=student.task_name,
            )
        self._search_model.write_editdistances(students_ed, save_path)
