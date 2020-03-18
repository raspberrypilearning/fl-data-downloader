import re

from .credentials import login, NeedToLoginException
from datetime import datetime
from mechanicalsoup import LinkNotFoundError

import pandas as pd

def get_courses(b, organisation):
    """
    Get all the FutureLearn courses for an organisation
    
    Returns the data as a `pandas.DataFrame`:
        + course - the short "name" for the course e.g. "programming-101"
        + full_name - the full name of the course

    :param Browser b:
        A browser object returned by the login function.
    
    :param string organisation:
        The organisation to get the courses for e.g. "raspberry-pi"
    
    :return:
        The course data in a `pandas.DataFrame`.
        
    """
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
    # courses_df.set_index("course", inplace=True)

    return courses_df

def get_runs(b, organisation):
    """
    Get all the runs for a course for an organisation 
    
    Returns the data as a `pandas.DataFrame`:
        + course - the short "name" for the course e.g. "programming-101"
        + full_name - the full name of the course
        + run - the run number
        + start_date - the date the run started
        + status - the current status of the run

    :param Browser b:
        A browser object returned by the login function.
    
    :param string organisation:
        The organisation to get the runs for e.g. "raspberry-pi"
    
    :return:
        The run data in a `pandas.DataFrame`.
    """
    url = "https://www.futurelearn.com/admin/organisations/{}/runs".format(organisation)
    response = _get_futurelearn_page(b, url)
    form = b.select_form('form[class="m-table-filter__checkboxes"]')

    course_runs = []
    
    # find the courses
    courses = re.findall(b"course-meta__title(.+?)\n(.+?)\n(.+?)\n(.+?)\n(.+?)\n(.+?)\n(.+?)\n(.+?)data-order(.+?)\n(.+?)\n",response.content)

    for each in courses:
        url_name = re.search(b'/courses/(.+?)/',each[0]).group(0).decode("utf-8")[:-1][9:]
        full_name = re.search(b'">(.+?)</a>',each[0]).group(0).decode("utf-8")[:-4][2:]
        run = int(re.search(b'/courses/(.+?)/(.+?)">',each[0]).group(0).decode("utf-8")[:-2].split("/")[-1])
        start_date = datetime.strptime(re.search(b"'(.+?)'",each[8]).group(0)[1:][:-1].decode("utf-8"),'%Y-%m-%d').date()
        status = re.search(b'flag--(.+?)>(.+?)<',each[5]).group(0)[:-1].decode("utf-8").split(">")[1]

        course_runs.append([url_name, full_name, run, start_date, status])
        # get the steps as well ?!
        #steps = get_steps_for_run(b, url_name, run)
        #course_runs.append([url_name, full_name, run, start_date, status, len(steps.index)])

    # course_runs_df = pd.DataFrame(course_runs, columns=["course", "full_name", "run_num", "start_date", "status", "no_of_steps"])
    course_runs_df = pd.DataFrame(course_runs, columns=["course", "full_name", "run", "start_date", "status"])
    # course_runs_df.set_index("course", "run_num", inplace=True)

    return course_runs_df

def get_steps_for_run(b, course, run):
    """
    Get the steps for a course run
    
    Returns the data as a `pandas.DataFrame`:
        + course - the short "name" for the course e.g. "programming-101"
        + run - the run number
        + step_id - the step id formated as `week.step`
        + week - the week the step belongs too
        + step - the number of the step
        + admin_url - the url to reach the admin page of the step
        + step_type - the type of step e.g. "article"

    :param Browser b:
        A browser object returned by the login function.
    
    :param string course:
        The online course e.g. "programming-101"

    :param integer run:
        The number of the specific course run 
    
    :return:
        The step data in a `pandas.DataFrame`.
    """
    print("course_run_steps.{}.{}".format(course, run))
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

def get_steps_for_courses(b, organisation, courses=None):
    """
    Get the steps for a list of courses.
    
    Returns the data as a `pandas.DataFrame`:
        + course - the short "name" for the course e.g. "programming-101"
        + run - the run number
        + step_id - the step id formated as `week.step`
        + week - the week the step belongs too
        + step - the number of the step
        + admin_url - the url to reach the admin page of the step
        + step_type - the type of step e.g. "article"

    :param Browser b:
        A browser object returned by the login function.
    
    :param string course:
        The online course e.g. "programming-101"

    :param integer run:
        The number of the specific course run 
    
    :return:
        The step data in a `pandas.DataFrame`.

    .. note::
        If `courses` is `None` (default), all courses for the organisation are returned

    """
    # get all the runs 
    runs_df = get_runs(b, organisation)
    steps_df = None

    # get the courses from the runs 
    if courses is None:
        courses = runs_df["course"].unique()

    first_run = True
    for course in courses:

        runs = runs_df[runs_df["course"] == course]["run"].to_list()

        for run in runs:
            if first_run:
                steps_df = get_steps_for_run(b, course, run)
                first_run = False
            else:
                steps_df = steps_df.append(get_steps_for_run(b, course, run), ignore_index=True)
    
    return steps_df

def _get_futurelearn_page(b, url):
    try:
        response = b.open(url)
        # select the sign out form, if it cant be its because they need to sign in
        form = b.select_form('form[class="m-admin-bar__sign-out-form"]')
        return response
        
    except LinkNotFoundError:
        raise NeedToLoginException("A mechanicalsoup.LinkNotFoundError was raised. Is your username and password correct? Does this organisation/course/run exist?")