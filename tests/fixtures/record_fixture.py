from datetime import datetime, timedelta

from tests.fakes.fake_commit import FakeCommit, FakeStats

dummy_dt = datetime(2019, 3, 30, 1, 1, 0, 0)

datetimes = [
    dummy_dt - timedelta(seconds=3),
    dummy_dt - timedelta(seconds=6),
    dummy_dt - timedelta(seconds=9),
]

hexshas = [
    "991dcb1ae434ffba832c0ad50b890afac7311111",
    "991dcb1ae434ffba832c0ad50b890afac731222",
    "991dcb1ae434ffba832c0ad50b890afac7313333",
]


student_records = []
for dt, sha in zip(datetimes, hexshas):
    record = FakeCommit(dt, sha)
    stats = FakeStats("tugas-tif.txt", 3, 1)
    record.stats = stats
    student_records.append(record)
