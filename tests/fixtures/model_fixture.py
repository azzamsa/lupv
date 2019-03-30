import git
import os.path as osp
from tests.fixtures import record_fixture

from tests.fixtures import search_controller_fixture as scf


def fake_student_dirs():
    """Fake the student directories."""
    return ["ani-1111", "budi-2222"]


def fake_get_records(student_path):
    """Fake the student commit records. Use commit from this repo instead.

    Using commit from this repo instead of real commit in
    /test/student_tasks/ help avoid using external testing dependencies,
    but in the end real commit still need to be used cause of
    faking git commit is not an easy task.
    """
    repo_path = osp.dirname(__file__)
    student_repo = git.Repo(repo_path, search_parent_directories=True)
    records = list(student_repo.iter_commits("master", max_count=5))
    return records


def fake_fake_get_records(student_path):
    # FIXME
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
