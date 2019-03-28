from collections import defaultdict

students = [
    {
        "name": "budi",
        "student_id": "2222",
        "filename": "tugas-tif.txt",
        "insertions": 13,
        "date": "Thu, 21 Mar 2019, 20:37:00",
    },
    {
        "name": "ani",
        "student_id": "1111",
        "filename": "tugas-tif.txt",
        "insertions": 13,
        "date": "Fri, 22 Mar 2019, 08:07:48",
    },
    {
        "name": "ani",
        "student_id": "1111",
        "filename": "tugas-tif.txt",
        "insertions": 13,
        "date": "Fri, 22 Mar 2019, 08:07:48",
    },
]

student_ips = [
    {
        "ip": "22.2.2222",
        "name": "budi",
        "student_id": "2222",
        "date": "Tue, 26 Mar 2019, 14:08:30",
    },
    {
        "ip": "22.2.2222",
        "name": "budi",
        "student_id": "2222",
        "date": "Tue, 26 Mar 2019, 14:08:24",
    },
    {
        "ip": "22.2.2222",
        "name": "budi",
        "student_id": "2222",
        "date": "Tue, 26 Mar 2019, 14:08:21",
    },
    {
        "ip": "22.2.2222",
        "name": "budi",
        "student_id": "2222",
        "date": "Tue, 26 Mar 2019, 14:08:18",
    },
    {
        "ip": "111.111.111",
        "name": "ani",
        "student_id": "1111",
        "date": "Tue, 26 Mar 2019, 13:52:48",
    },
    {
        "ip": "111.111.111",
        "name": "ani",
        "student_id": "1111",
        "date": "Tue, 26 Mar 2019, 13:52:45",
    },
    {
        "ip": "111.111.111",
        "name": "ani",
        "student_id": "1111",
        "date": "Tue, 26 Mar 2019, 13:52:42",
    },
    {
        "ip": "111.111.111",
        "name": "ani",
        "student_id": "1111",
        "date": "Tue, 26 Mar 2019, 13:52:38",
    },
]

grouped_students = defaultdict(
    list,
    {
        "22.2.2222": [
            {
                "ip": "22.2.2222",
                "name": "budi",
                "student_id": "2222",
                "date": "Tue, 26 Mar 2019, 14:08:30",
            },
            {
                "ip": "22.2.2222",
                "name": "budi",
                "student_id": "2222",
                "date": "Tue, 26 Mar 2019, 14:08:24",
            },
            {
                "ip": "22.2.2222",
                "name": "budi",
                "student_id": "2222",
                "date": "Tue, 26 Mar 2019, 14:08:21",
            },
            {
                "ip": "22.2.2222",
                "name": "budi",
                "student_id": "2222",
                "date": "Tue, 26 Mar 2019, 14:08:18",
            },
        ],
        "111.111.111": [
            {
                "ip": "111.111.111",
                "name": "ani",
                "student_id": "1111",
                "date": "Tue, 26 Mar 2019, 13:52:48",
            },
            {
                "ip": "111.111.111",
                "name": "ani",
                "student_id": "1111",
                "date": "Tue, 26 Mar 2019, 13:52:45",
            },
            {
                "ip": "111.111.111",
                "name": "ani",
                "student_id": "1111",
                "date": "Tue, 26 Mar 2019, 13:52:42",
            },
            {
                "ip": "111.111.111",
                "name": "ani",
                "student_id": "1111",
                "date": "Tue, 26 Mar 2019, 13:52:38",
            },
        ],
    },
)
