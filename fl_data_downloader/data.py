import csv
import os
import re

import pandas as pd
from mechanicalsoup import LinkNotFoundError

from requests.exceptions import ConnectionError

from datetime import datetime, timedelta, date
from io import StringIO
from time import sleep

from .credentials import login
from .exceptions import (
    NeedToLoginException, 
    DatasetNotKnownException, 
    DatasetNotFoundForCourse, 
    CourseRunNotFound,
    ConnectionErrorMaxRetriesExceeded
)
from .cache import CacheManager

STATS_URL = "https://www.futurelearn.com/admin/courses/{course}/{run}/stats-dashboard/data/{dataset}"
COUNTRIES_DEMOGRAPHICS_URL = "https://www.futurelearn.com/admin/courses/{course}/{run}/demographics/countries/{dataset}-dataset"

DATASET_URLS = {
    "archetype_survey_responses": STATS_URL,
    "campaigns": STATS_URL,
    "comments": STATS_URL,
    "countries": COUNTRIES_DEMOGRAPHICS_URL,
    "country-subdivisions": COUNTRIES_DEMOGRAPHICS_URL,
    "enrolments": STATS_URL,
    "leaving_survey_responses": STATS_URL,
    "peer_review_assignments": STATS_URL,
    "peer_review_reviews": STATS_URL,
    "post_course_survey_data": STATS_URL,
    "post_course_survey_free_text": STATS_URL,
    "question_response": STATS_URL,
    "step_activity": STATS_URL,
    "team_members": STATS_URL,
    "video_stats": STATS_URL,
    "weekly_sentiment_survey_responses": STATS_URL
}

AVAILABLE_DATASETS = DATASET_URLS.keys()

# a course run is inactive after this time from the start date 
# datasets are no longer downloaded if in cache for inactive courses
#  12 weeks
COURSE_RUN_INACTIVE_AFTER = 12 * 7 * 24 * 60 * 60

# after how long does the cache expiry if the course is active
#  12 hours
CACHE_EXPIRY_TIME = 12 * 60 *60
# debug - make cache expire after 1 second
# CACHE_EXPIRY_TIME = 1

# the time to wait after a ConnectionError before retrying
RETRY_TIME = 30

class FutureLearnData:
    """
    Supports the retrieval of data from FutureLearn, including datasets
    from course stats and course meta data.

    Examples.
    
    1) Get a list of courses for the "raspberry-pi" organisation::

        from fl_data_downloader import FutureLearnData

        fl = FutureLearnData("raspberry-pi")

        courses_df = fl.get_courses()

        print(courses_df)

    2) Get the enrolment dataset for the `programming-101` course ::

        from fl_data_downloader import FutureLearnData

        fl = FutureLearnData("raspberry-pi")

        enrolments_df = fl.get_dataset_for_course(course="programming-101", dataset="enrolments")

        print(enrolments_df)

    A list of available datasets can be obtained using::
    
        from fl_data_downloader import AVAILABLE_DATASETS
        print(AVAILABLE_DATASETS)

    Information about available datasets can be found at https://futurelearnpartnersupport.zendesk.com/hc/en-us/articles/360035051173-Datasets

    :param Browser browser:
        A browser object returned by the `fl_data_downloader.login` function. 
        If `None` (default) the login function will be called.
    
    :param string organisation:
        The organisation to get the courses for e.g. "raspberry-pi"
    
    :param boolean use_cache:
        Whether to use the cache. Defaults to `True`.

    :param string cache_directory:
        The directory to use for storing cache files. If `None` (default)
        the directory ~/.fl-data-dl-cache

    :param integer max_retries:
        The maximum number of times to try and download a dataset 
    """
    def __init__(self, organisation, browser=None, use_cache=True, cache_directory=None, max_retries=3):
        
        self._organisation = organisation
        self._cache_manager = CacheManager(cache_directory, use_cache)
        self._cache_directory = cache_directory
        self._use_cache = use_cache
        self._max_retries = max_retries

        if browser is None:
            browser = login()
        self._browser = browser

        # a property which will hold all the runs for the organisation
        self._runs = None

        # the number of failed requests in a row
        self._failed_requests = 0

    def get_dataset(self, course, run, dataset):
        """
        Gets a FutureLearn dataset for a specific run of a course.

        :param string course:
            The online course e.g. "programming-101"

        :param integer run:
            The number of the specific course run 

        :param string dataset:
            The name of the dataset e.g. "enrolments"
        
        :return:
            The dataset in a `pandas.DataFrame`.
        """

        expiry = self._calc_cache_expiry(dataset, self.get_run_active_status(course, run))
        
        df = self._cache_manager.get_data(self._organisation, course, run, dataset, expiry=expiry)
        if df is None:

            # get the campaign data file
            url = DATASET_URLS[dataset].format(course=course, run=run, dataset=dataset)
            downloaded = False
            while not downloaded:
                print("downloading   - {}_{}_{}_{}".format(self._organisation, course, run, dataset))
                try:
                    data = self._browser.open(url)
                    self._failed_requests = 0
                    downloaded = True
                except ConnectionError as e:
                    self._failed_requests += 1
                    if self._failed_requests < self._max_retries:
                        print("error - ConnectionError occurred - {}. Retrying in {} secs.".format(e, RETRY_TIME))
                        sleep(RETRY_TIME)
                    else:
                        raise ConnectionErrorMaxRetriesExceeded("ConnectionError occurred. Max number of retries exceeded.")

            data = data.content.decode("utf-8").strip()

            # has a html page been returned? if so, you need to login
            if data[0].find("<!DOCTYPE html>") > -1:
                raise NeedToLoginException()
            
            df = pd.read_csv(StringIO(data))

            # add the course and run columns
            df.insert(0, "course", course)
            df.insert(1, "run", run)

            self._cache_manager.save_data(df, self._organisation, course, run, dataset)
        
        return df

    def get_dataset_for_course(self, course, dataset):
        """
        Gets a FutureLearn dataset for all runs of a course

        :param string course:
            The online course e.g. "programming-101"

        :param string dataset:
            The name of the dataset e.g. "enrolments"
        
        :return:
            The dataset in a `pandas.DataFrame`.
        """

        runs_df = self.runs
        runs = runs_df[runs_df["course"] == course]["run"].sort_values().to_list()

        df = None
        first_run = True
        for run in runs:
            try:
                if first_run:
                    df = self.get_dataset(course, run, dataset)
                    first_run = False
                else:
                    df = df.append(self.get_dataset(course, run, dataset), ignore_index=True)

            except LinkNotFoundError:
                if first_run:
                    raise DatasetNotFoundForCourse
                break

        return df

    def get_dataset_for_courses(self, courses, dataset):
        """
        Gets a FutureLearn dataset for all runs of multiple courses
        
        :param List courses:
            A list of course names e.g. `["programming-101", "embedded-systems"]`

        :param string dataset:
            The name of the dataset e.g. "enrolments"
        
        :return:
            The dataset in a `pandas.DataFrame`.
        """
        first_course = True
        dataset_df = None
        
        for course in courses:
            try:
                dataset_for_course_df = self.get_dataset_for_course(course, dataset)
                if first_course:
                    dataset_df = dataset_for_course_df
                    first_course = False
                else:
                    dataset_df = dataset_df.append(dataset_for_course_df, ignore_index=True)
            except DatasetNotFoundForCourse:
                    print("dataset [{}] was not found for course [{}].".format(dataset, course))
            
        return dataset_df

    def get_courses(self):
        """
        Get all the FutureLearn courses for an organisation
        
        Returns the data as a `pandas.DataFrame`:
            + course - the short "name" for the course e.g. "programming-101"
            + full_name - the full name of the course

        :return:
            The course data in a `pandas.DataFrame`.            
        """
        expiry = self._calc_cache_expiry("courses", True)
        df = self._cache_manager.get_data(self._organisation, "courses", expiry=expiry)
        if df is None:
            print("downloading   - {}_courses".format(self._organisation))

            # pull the unique runs and descriptions from the course runs
            df = self.runs[["course", "full_name"]].drop_duplicates()
            df.reset_index(drop=True, inplace=True)
            self._cache_manager.save_data(df, self._organisation, "courses")

        return df

    def get_runs(self):
        """
        Get all the runs for an organisation 
        
        Returns the data as a `pandas.DataFrame`:
            + course - the short "name" for the course e.g. "programming-101"
            + full_name - the full name of the course
            + run - the run number
            + start_date - the date the run started
            + status - the current status of the run
        
        :return:
            The run data in a `pandas.DataFrame`.
        """
        expiry = self._calc_cache_expiry("runs", True)
        df = self._cache_manager.get_data(self._organisation, "runs", expiry=expiry)
        if df is None:
            print("downloading   - {}_runs".format(self._organisation))

            url = "https://www.futurelearn.com/admin/organisations/{}/runs".format(self._organisation)
            response = self._get_futurelearn_page(url)
            form = self._browser.select_form('form[class="m-table-filter__checkboxes"]')

            course_runs = []
            
            # find the courses
            courses = re.findall(b"course-meta__title(.+?)\n(.+?)\n(.+?)\n(.+?)\n(.+?)\n(.+?)\n(.+?)\n(.+?)data-order(.+?)\n(.+?)\n",response.content)

            for each in courses:
                url_name = re.search(b'/courses/(.+?)/',each[0]).group(0).decode("utf-8")[:-1][9:]
                full_name = re.search(b'">(.+?)</a>',each[0]).group(0).decode("utf-8")[:-4][2:]
                run = int(re.search(b'/courses/(.+?)/(.+?)">',each[0]).group(0).decode("utf-8")[:-2].split("/")[-1])
                # start_date = datetime.strptime(re.search(b"'(.+?)'",each[8]).group(0)[1:][:-1].decode("utf-8"),'%Y-%m-%d').date()
                start_date = re.search(b"'(.+?)'",each[8]).group(0)[1:][:-1].decode("utf-8")
                status = re.search(b'flag--(.+?)>(.+?)<',each[5]).group(0)[:-1].decode("utf-8").split(">")[1]

                course_runs.append([url_name, full_name, run, start_date, status])

            df = pd.DataFrame(course_runs, columns=["course", "full_name", "run", "start_date", "status"])

            self._cache_manager.save_data(df, self._organisation, "runs")

        return df

    def get_steps_for_run(self, course, run):
        """
        Get the steps for a course run
        
        Returns the data as a `pandas.DataFrame`:
            + course - the short "name" for the course e.g. "programming-101"
            + run - the run number
            + step_id - the step id formated as `week.step`
            + week - the week the step belongs too
            + step - the number of the step
            + admin_url - the url to reach the admin page of the step
            + step_type - the type of step e.g. "article" (article, discussion, video-article, quizze, exercise, assignment, assignment_review, assignment_reflection)

        :param string course:
            The online course e.g. "programming-101"

        :param integer run:
            The number of the specific course run 
        
        :return:
            The step data in a `pandas.DataFrame`.
        """
        expiry = self._calc_cache_expiry("steps-for-run", self.get_run_active_status(course, run))
        df = self._cache_manager.get_data(self._organisation, course, run, "steps-for-run", expiry=expiry)
        
        if df is None:
            print("downloading   - {}_{}_{}_steps-for-run".format(self._organisation, course, run))

            url = "https://www.futurelearn.com/admin/courses/{}/{}/overview#step-types".format(course, run)
            response = self._get_futurelearn_page(url)
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

            df = pd.DataFrame(run_steps, columns=["course", "run", "step_id", "week", "step", "admin_url", "step_type"])

            self._cache_manager.save_data(df, self._organisation, course, run, "steps-for-run")

        return df

    def get_steps_for_courses(self, courses=None):
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
        
        :param List courses:
            A list of online courses e.g. ["programming-101", "code-club"]

        :return:
            The step data in a `pandas.DataFrame`.

        .. note::
            If `courses` is `None` (default), all courses for the organisation are returned

        """
        # get all the runs 
        runs_df = self.get_runs()
        steps_df = None

        # get the courses from the runs 
        if courses is None:
            courses = runs_df["course"].unique()

        first_run = True
        for course in courses:

            runs = runs_df[runs_df["course"] == course]["run"].to_list()

            for run in runs:
                if first_run:
                    steps_df = self.get_steps_for_run(course, run)
                    first_run = False
                else:
                    steps_df = steps_df.append(self.get_steps_for_run(course, run), ignore_index=True)
        
        return steps_df

    @property
    def runs(self):
        """
        In-memory cache of course runs for the organisation. Loaded when first
        called. `get_runs()` can be used to pull this data back.
        """
        # get the runs if it hasn't been already
        if self._runs is None:
            self._runs = self.get_runs()
        return self._runs

    def get_run_active_status(self, course, run):
        """
        Returns whether a run is still "active" and therefore data is still 
        being updated. A course is deemed "inactive" if the run started over 12 weeks ago. 
        
        :param string course:
            The online course e.g. "programming-101"

        :param integer run:
            The number of the specific course run 
        
        :return:
            True is the course is "active", False if "inactive".
        """
        # get the course run
        run_df = self.runs[(self.runs["course"] == course) & (self.runs["run"] == run)]

        if run_df.empty:
            raise CourseRunNotFound("The course run does not exist. {}.{}".format(course, run))
        
        # calculate the date the run expires
        start_date = run_df.iloc[0]["start_date"]
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        expired_date = start_date + timedelta(seconds=COURSE_RUN_INACTIVE_AFTER)
        
        return datetime.now() < expired_date

    def _get_futurelearn_page(self, url):
        try:
            response = self._browser.open(url)
            # select the sign out form, if it cant be its because they need to sign in
            form = self._browser.select_form('form[class="m-admin-bar__sign-out-form"]')
            return response
            
        except LinkNotFoundError:
            print(error)
            raise NeedToLoginException("A mechanicalsoup.LinkNotFoundError was raised. Is your username and password correct? Does this organisation/course/run exist?")
    
    def _calc_cache_expiry(self, dataset, active):
        # the cache expiry is in 12 hours before now (i.e. any cache older than 12 hours will be refreshed)
        # unless the run is no longer active and its not the enrolments data (which is always refreshed)
        if (dataset != "enrolments" and not active):
            expiry = None
        else:
            expiry = datetime.now() - timedelta(seconds=CACHE_EXPIRY_TIME)

        return expiry

def download_data(organisation, courses, datasets=None, directory=".", use_cache=True):
    """
    Downloads dataset data for all runs of a course and saves to a CSV file(s).

    Information about available datasets can be found at https://futurelearnpartnersupport.zendesk.com/hc/en-us/articles/360035051173-Datasets

    :param List courses:
        A list of course names e.g. `["programming-101", "embedded-systems"]`

    :param string datasets :
        The list of dataset names of the dataset e.g. ["enrolments", "step_activity"]. If `None` (the default) all datasets will be downloaded.
    
    :return:
        Returns a list of file paths containing the downloaded data.
    """
    fl = FutureLearnData(organisation, use_cache=use_cache, max_retries=1)
    
    files = []

    # if a dataset is not provided, download for all datasets
    if datasets is None:
        datasets = AVAILABLE_DATASETS

    for dataset in datasets:
        if dataset in AVAILABLE_DATASETS:
            # create file path
            file_path = os.path.join(directory, "{}_{}.csv".format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"), dataset))
            print("Filename: {}".format(file_path))

            # delete any old files - belt and braces!
            if os.path.exists(file_path):
                print("- deleting old dataset")
                os.remove(file_path)

            # download the dataset for each course
            first_course = True
            for course in courses:
               
                try:
                    dataset_df = fl.get_dataset_for_course(course, dataset)
                    dataset_df.to_csv(file_path, mode="a", header=first_course, index=False)
                    files.append(file_path)

                    first_course = False

                except DatasetNotFoundForCourse:
                    print("Error: dataset [{}] was not found for course [{}].".format(dataset, course))
        else:
            raise DatasetNotKnownException()

    return files
