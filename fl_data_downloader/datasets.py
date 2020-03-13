import csv
import os
import mechanicalsoup

import pandas as pd

from datetime import datetime
from io import StringIO
from collections import namedtuple

from .credentials import login
from .exceptions import NeedToLoginException, DatasetNotKnownException, DatasetNotFoundForCourse


URL = "https://www.futurelearn.com/admin/courses/{}/{}/stats-dashboard/data/{}"
DATASETS = [
    "archetype_survey_responses",
    "campaigns",
    "comments",
    "enrolments",
    "leaving_survey_responses",
    "peer_review_assignments",
    "peer_review_reviews",
    "post_course_survey_data",
    "post_course_survey_free_text",
    "question_response",
    "step_activity",
    "team_members",
    "video_stats",
    "weekly_sentiment_survey_responses"
]

DATASET_KEYS = {
    "archetype_survey_responses": ["course", "run", "id"],
    "comments": ["course", "run", "id"],
    "campaigns": ["course", "run", "utm_source", "utm_campaign", "utm_medium", "utm_term", "utm_content", "domain"],
    "enrolments": ["course", "run", "learner_id"],
    "leaving_survey_responses": ["course", "run", "id"],
    "peer_review_assignments": ["course", "run", "id"],
    "peer_review_reviews": ["course", "run", "id"],
    "post_course_survey_data": ["course", "run", "id"],
    "post_course_survey_free_text": ["course", "run"],
    "question_response": ["course", "run"],
    "step_activity": ["course", "run", "learner_id", "step"],
    "team_members": ["course", "run", "id"],
    "video_stats": ["course", "run", "step_position"],
    "weekly_sentiment_survey_responses": ["course", "run", "id"],
    }

def get_dataset(b, course, run, dataset):
    """
    Gets a dataset for a specific run of a course

    Returns a `pandas.DataFrame`.
    """

    print("{}.{}.{}".format(dataset, course, run))

    # get the campaign data file
    url = URL.format(course, run, dataset)
    data = b.open(url)
    data = data.content.decode("utf-8").strip()

    # has a html page been returned? if so, you need to login
    if data[0].find("<!DOCTYPE html>") > -1:
        raise NeedToLoginException()
    
    dataset_df = pd.read_csv(StringIO(data))

    # add the course and run columns
    dataset_df.insert(0, "course", course)
    dataset_df.insert(1, "run", run)

    # set and index of the keys?
    # dataset_df.set_index(DATASET_KEYS[dataset], inplace=True)

    return dataset_df
    
def get_dataset_for_course(b, course, dataset):
    """
    Gets the dataset from all runs of a course

    Returns a `pandas.DataFrame`.
    """
    run = 1
    while True:
        try:
            if run == 1:
                dataset_df = get_dataset(b, course, run, dataset)
            else:
                dataset_df = dataset_df.append(get_dataset(b, course, run, dataset), ignore_index=True)

        except mechanicalsoup.LinkNotFoundError:
            if run == 1:
                raise DatasetNotFoundForCourse
            break
            
        run += 1
    
    return dataset_df

def get_dataset_for_courses(b, courses, dataset):
    """
    Gets the dataset from all runs of multiple courses

    Returns a `pandas.DataFrame`.
    """
    first_course = True
    dataset_df = None
    
    for course in courses:
        try:
            dataset_for_course_df = get_dataset_for_course(b, course, dataset)
            if first_course:
                dataset_df = dataset_for_course_df
                first_course = False
            else:
                dataset_df = dataset_df.append(dataset_for_course_df, ignore_index=True)
        except DatasetNotFoundForCourse:
                print("dataset [{}] was not found for course [{}].".format(dataset, course))
        
    return dataset_df

def download_data(courses, datasets=None, directory="."):
    """
    Downloads dataset data for all runs of a course and saves to a CSV file.

    Returns a list of file paths.
    """
    b = login()
    files = []

    # if a dataset is not provided, download for all datasets
    if datasets is None:
        datasets = DATASETS

    for dataset in datasets:
        if dataset in DATASETS:
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
                    dataset_df = get_dataset_for_course(b, course, dataset)
                    dataset_df.to_csv(file_path, mode="a", header=first_course)
                    files.append(file_path)

                    first_course = False

                except DatasetNotFoundForCourse:
                    print("Error: dataset [{}] was not found for course [{}].".format(dataset, course))
        else:
            raise DatasetNotKnownException()

    return files
