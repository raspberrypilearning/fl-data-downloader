import re

from .credentials import login, NeedToLoginException
from datetime import datetime
from mechanicalsoup import LinkNotFoundError

import pandas as pd

def get_courses(b, organisation="raspberry-pi"):
    url = "https://www.futurelearn.com/admin/organisations/{}/runs".format(organisation)
    response = _get_futurelearn_page(b, url)
    # response = b.open(url)
    form = b.select_form('form[class="m-table-filter__checkboxes"]')

    unique_courses = {}
    
    courses = re.findall(b"course-meta__title(.+?)\n(.+?)\n(.+?)\n(.+?)\n(.+?)\n(.+?)\n(.+?)\n(.+?)data-order(.+?)\n(.+?)\n",response.content)

    for each in courses:
        url_name = re.search(b'/courses/(.+?)/',each[0]).group(0).decode("utf-8")[:-1][9:]
        if url_name not in unique_courses.keys():
            full_name = re.search(b'">(.+?)</a>',each[0]).group(0).decode("utf-8")[:-4][2:]
            unique_courses[url_name] = full_name

    courses_df = pd.DataFrame(unique_courses.items(), columns=["course", "full_name"])
    courses_df.set_index("course", inplace=True)

    return courses_df

def get_runs(b, course=None, organisation="raspberry-pi"):
    url = "https://www.futurelearn.com/admin/organisations/{}/runs".format(organisation)
    response = _get_futurelearn_page(b, url)
    form = b.select_form('form[class="m-table-filter__checkboxes"]')

    course_runs = []
    
    courses = re.findall(b"course-meta__title(.+?)\n(.+?)\n(.+?)\n(.+?)\n(.+?)\n(.+?)\n(.+?)\n(.+?)data-order(.+?)\n(.+?)\n",response.content)

    for each in courses:
        url_name = re.search(b'/courses/(.+?)/',each[0]).group(0).decode("utf-8")[:-1][9:]
        if course is not None and course == url_name:
            full_name = re.search(b'">(.+?)</a>',each[0]).group(0).decode("utf-8")[:-4][2:]
            run_num = int(re.search(b'/courses/(.+?)/(.+?)">',each[0]).group(0).decode("utf-8")[:-2].split("/")[-1])
            print("Run - {}/{}".format(url_name, run_num))
            start_date = datetime.strptime(re.search(b"'(.+?)'",each[8]).group(0)[1:][:-1].decode("utf-8"),'%Y-%m-%d').date()
            status = re.search(b'flag--(.+?)>(.+?)<',each[5]).group(0)[:-1].decode("utf-8").split(">")[1]

            course_runs.append([url_name, full_name, run_num, start_date, status])
            # get the steps as well ?!
            #steps = get_run_steps(b, url_name, run_num)
            #course_runs.append([url_name, full_name, run_num, start_date, status, len(steps.index)])

    # course_runs_df = pd.DataFrame(course_runs, columns=["course", "full_name", "run_num", "start_date", "status", "no_of_steps"])
    course_runs_df = pd.DataFrame(course_runs, columns=["course", "full_name", "run_num", "start_date", "status"])
    course_runs_df.set_index("course", "run_num", inplace=True)

    return course_runs_df

def get_run_steps(b, course, run):

    url = "https://www.futurelearn.com/admin/courses/{}/{}/overview#step-types".format(course, run)
    response = _get_futurelearn_page(b, url)
    raw_page = response.content
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
            step_type = key[:-1]
            run_steps.append([course, run, step_id, week, step, admin_url, step_type])

    return pd.DataFrame(run_steps, columns=["course", "run", "step_id", "week", "step", "admin_url", "step_type"])

def _get_futurelearn_page(b, url):
    try:
        response = b.open(url)
        # select the sign out form, if it cant be its because they need to sign in
        form = b.select_form('form[class="m-admin-bar__sign-out-form"]')
        return response
        
    except LinkNotFoundError:
        raise NeedToLoginException("A mechanicalsoup.LinkNotFoundError was raised. Is your username and password correct?")