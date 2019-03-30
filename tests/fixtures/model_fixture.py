import git
from tests.fixtures import record_fixture

from tests.fixtures import search_controller_fixture as scf


def fake_student_dirs():
    """Fake the student directories."""
    return ["ani-1111", "budi-2222"]


def fake_get_records(student_path):
    return record_fixture.student_records


def fake_student_repo(student_path):
    """Fake the initialize student_repo to avoid using
    on_current_student_dir_changed that invoke a lot of thing
    other than just initialize the student_repo.
    """
    student_repo = git.Repo(student_path)
    return student_repo


def fake_read_editdistances(filename):
    return scf.students_ed
