import os.path as osp


def fixture_path(name):
    return osp.join(osp.dirname(osp.dirname(__file__)), "tests", "fixtures", name)


def fixture(name):
    with open(fixture_path(name), "rb") as infile:
        return infile.read()
