from datetime import datetime, timedelta

from tests.fixtures import record_fixture
from tests.fixtures import search_controller_fixture as scf
from tests.fixtures import view_fixture as vf
from tests.helper import fixture


sample_delta_dt = datetime(2019, 3, 30, 1, 1, 0, 0) - timedelta(hours=1)
sample_delta_dt_2 = datetime(2019, 3, 30, 1, 1, 0, 0) - timedelta(hours=-1)

#
# MainController
#


def fake_get_first_record_time(first_record_dt):
    first_record_time = "Tue, 26 Mar 2019, 13:52:38"
    first_record_relativetime = "2 days ago"
    return first_record_time, first_record_relativetime


def fake_get_last_record_time(last_record_dt):
    last_record_time = "Tue, 26 Mar 2019, 13:52:48"
    last_record_relativetime = "1 day ago"
    return last_record_time, last_record_relativetime


def fake_calc_work_duration(first_record_dt, last_record_dt):
    work_duration = "0:00:10"
    work_relative_duration = "10 seconds"
    return work_duration, work_relative_duration


def fake_populate_students_records():
    return vf.student_records


#
# LogController
#


def fake_read_files():
    return ["tugas-tif.txt"]


def fake_read_auth_info(sha):
    return ["ani", "ani-machine", "111.111.111"]


def fake_read_all_windows(sha):
    return [
        "emacs@screencast",
        "FrontPage - Python Wiki - Firefox Developer Edition",
        "bash",
    ]


def fake_read_focused_window(sha):
    return "bash"


def fake_read_diff(filename, sha):
    return fixture("ani_diff").decode()


def fake_take_diff_body(diff):
    return " ani 1\n+ani 2"


def fake_wrap_with_html(diff):
    return fixture("colored_diff").decode()


def fake_is_exists(filename, sha):
    return True


def fake_read_file(filename, sha):
    return "ani 1\nani 2"


#
# SearchController
#


def fake_get_diff(filename, sha):
    return " ani 1<br/><span style='color:green;white-space:pre;'>+ani 2</span>"


def fake_student_directories_iterator():
    student_dirs = ["ani-1111", "budi-2222"]

    for student_dir in student_dirs:
        yield student_dir


def fake_record_iterator():
    student_dir = "ani-1111"
    records = record_fixture.student_records

    for record in records:
        yield student_dir, record


def fake_record_iterator_suspect():
    student_dir = "budi-2222"
    records = record_fixture.student_record_suspect

    for record in records:
        yield student_dir, record


def fake_get_student_ips():
    return scf.student_ips


def fake_group_by_id(students_ip):
    return scf.grouped_students


def fake_multigroup_child(student_group):
    return scf.multigroup_students


def fake_collect_student_windows(search_key):
    return scf.student_windows


def fake_create_lupvnotes_dir():
    pass


def fake_calc_editdistances(student_dir, filename):
    return "a", "b"


def fake_write_editdistances(student_ed, filename):
    pass


def fake_construct_editdistance_path(filename):
    return "home/x/student_tasks/lupv-notes/ed.text"
