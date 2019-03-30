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

#
# student records
#

student_records = []
for dt, sha in zip(datetimes, hexshas):
    record = FakeCommit(dt, sha)
    stats = FakeStats("tugas-tif.txt", 3, 1)
    record.stats = stats
    student_records.append(record)


#
# student records with exceeded insertions
#


student_record_suspect = []
record_s = FakeCommit(dt, "991dcb1ae434ffba832c0ad50b890afac7318888")
stats_s = FakeStats("tugas-tif.txt", 20, 1)
record_s.stats = stats_s
student_record_suspect.append(record_s)
student_record_suspect.extend(student_records)


#
# student records wrapped into dictionary
#


student_records_2 = [
    {"name": "budi", "student_id": "2222", "records": student_records},
    {"name": "ani", "student_id": "1111", "records": student_records},
]
