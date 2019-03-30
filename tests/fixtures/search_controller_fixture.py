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
            }
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
        ],
    },
)

multigroup_students = {
    "22.2.2222": defaultdict(
        list,
        {
            "budi-2222": [
                {
                    "ip": "22.2.2222",
                    "name": "budi",
                    "student_id": "2222",
                    "date": "Tue, 26 Mar 2019, 14:08:30",
                }
            ]
        },
    ),
    "111.111.111": defaultdict(
        list,
        {
            "ani-1111": [
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
            ]
        },
    ),
}

student_windows = [
    {
        "window_name": "FrontPage - Python Wiki - Firefox Developer Edition",
        "name": "ani",
        "student_id": "1111",
        "date": "Sat, 30 Mar 2019, 01:00:57",
    },
    {
        "window_name": "FrontPage - Python Wiki - Firefox Developer Edition",
        "name": "ani",
        "student_id": "1111",
        "date": "Sat, 30 Mar 2019, 01:00:54",
    },
    {
        "window_name": "FrontPage - Python Wiki - Firefox Developer Edition",
        "name": "budi",
        "student_id": "2222",
        "date": "Sat, 30 Mar 2019, 01:00:51",
    },
]

students_ed = {
    "budi-2222": {
        "editdistances_ax": [0, 8, 30],
        "records_ax": [1, 2, 3],
        "task_name": "tugas-tif.txt",
    },
    "ani-1111": {
        "editdistances_ax": [0, 12, 831, 843, 856],
        "records_ax": [1, 2, 3, 4, 5],
        "task_name": "tugas-tif.txt",
    },
}
