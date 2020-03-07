import re

from credentials import login
from datetime import datetime

import pandas as pd

class Courses:
    def __init__(self, organisation="raspberry-pi"):
        self.organisation = organisation
    
    def get_courses(self, b=None):
        if b is None:
            b = login()

        url = "https://www.futurelearn.com/admin/organisations/{}/runs".format(self.organisation)
        response = b.open(url)
        form = b.select_form('form[class="m-table-filter__checkboxes"]')

        courses = {}
        
        courses = re.findall(b"course-meta__title(.+?)\n(.+?)\n(.+?)\n(.+?)\n(.+?)\n(.+?)\n(.+?)\n(.+?)data-order(.+?)\n(.+?)\n",response.content)

        for each in courses:
            full_name = re.search(b'">(.+?)</a>',each[0]).group(0).decode("utf-8")[:-4][2:]
            url_name = re.search(b'/courses/(.+?)/',each[0]).group(0).decode("utf-8")[:-1][9:]
            run_num = int(re.search(b'/courses/(.+?)/(.+?)">',each[0]).group(0).decode("utf-8")[:-2].split("/")[-1])
            print("Run - {}/{}".format(url_name, run_num))
            start_date = datetime.strptime(re.search(b"'(.+?)'",each[8]).group(0)[1:][:-1].decode("utf-8"),'%Y-%m-%d').date()
            status = re.search(b'flag--(.+?)>(.+?)<',each[5]).group(0)[:-1].decode("utf-8").split(">")[1]
            steps = self.get_run_steps(url_name, run_num, b)

            course_runs.append(CourseRun(full_name, run_num, start_date, status, url_name, steps))

        return course_runs

    def get_run_steps(self, name, run, b=None):
        if b is None:
            b = login()

        r = b.open("https://www.futurelearn.com/admin/courses/{}/{}/overview#step-types".format(name,run))
        raw_page = r.content
        search_keys = {
            "video-articles":b'video-articles/(.+?)VI',
            "discussions":b'discussions/(.+?)DI',
                "articles":b'/articles/(.+?)AR',
            "quizzes":b'quizzes/(.+?)QU',
            "exercises":b'exercises/(.+?)EX',
            "assignments":b'assignments/(.+?)AS',
            "assignment_reviews":b'assignment_reviews/(.+?)RV',
            "assignment_reflections":b'assignment_reflections/(.+?)RE',
            "poll_articles":b'poll-articles/(.+?)PL',
            "audio_articles":b'audio-articles/(.+?)AU',
            }

        run_steps = []
        # print(raw_page)
        for key in search_keys:

            raw_steps = re.findall(search_keys[key],raw_page)               
            # print(key, len(raw_steps))

            for raw_step in raw_steps:
                step_info = re.findall("(\d+)",raw_step.decode('utf-8'))
                # print(step_info)
                admin_url = "https://www.futurelearn.com/admin/{}/{}".format(key,step_info[0])

                step_id = step_info[1] + "." + step_info[2].zfill(2)
                week = step_info[1]
                step = step_info[2]
                run_steps.append(CourseStep(step_id, week, step, admin_url, key[:-1]))
        return run_steps

class Course():
    def __init__(self, name, full_name, runs):
        self.name = name
        self.full_name
        self.runs = []

class CourseRun:
    def __init__(self, name, run, start_date, status, steps):
        self.name = name
        self.run = run
        self.start_date = start_date
        self.status = status 
        self.steps = steps

    @property
    def no_of_steps(self):
        return len(self.steps)

    def __str__(self):
        print("Run - {}/{}".format(
            self.url_name,
            self.run
        ))

class CourseStep:
    def __init__(self, step_id, week, step, admin_url, step_type):
        self.step_id = step_id
        self.week = week
        self.step = step
        self.admin_url = admin_url
        self.step_type = step_type

courses = Courses()
runs = courses.get_runs()

for run in runs:
    print(run)


