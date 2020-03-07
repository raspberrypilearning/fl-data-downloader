import csv
import os
import mechanicalsoup

import pandas as pd

from datetime import datetime

from .credentials import login, NeedToLoginException

class DatasetNotKnownException(Exception):
    pass

class DatasetNotFoundForCourse(Exception):
    pass

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

def get_dataset(b, course, run, dataset):

    # get the campaign data file
    url = URL.format(course, run, dataset)
    data = b.open(url)
    data = data.content.decode("utf-8").strip()

    if data[0].find("<!DOCTYPE html>") > -1:
        raise NeedToLoginException()
    
    dataset = pd.read_csv(data)
    print(dataset)

    # open the file as a csv
    # datafilecsv = csv.reader(data.content.decode("utf-8").strip().split("\n"))

    # # get the first row
    # header_row = next(datafilecsv)
    
    # # has a html page been returned? if so, you need to login
    # if header_row[0].find("<!DOCTYPE html>") > -1:
    #     raise NeedToLoginException()

    # # append the course name and run number to the file
    # header_row.insert(0, "course")
    # header_row.insert(1, "run")

    # datasetrows = [header_row]
    # #print(datafilerows[0])
    
    # for row in datafilecsv:
    #     row.insert(0, course)
    #     row.insert(1, str(run))
    #     #print(row)
    #     datasetrows.append(row)
    
    # return datasetrows

def get_dataset_old(b, course, run, dataset):

    # get the campaign data file
    url = URL.format(course, run, dataset)
    data = b.open(url)
    
    # open the file as a csv
    datafilecsv = csv.reader(data.content.decode("utf-8").strip().split("\n"))

    # get the first row
    header_row = next(datafilecsv)
    
    # has a html page been returned? if so, you need to login
    if header_row[0].find("<!DOCTYPE html>") > -1:
        raise NeedToLoginException()

    # append the course name and run number to the file
    header_row.insert(0, "course")
    header_row.insert(1, "run")

    datasetrows = [header_row]
    #print(datafilerows[0])
    
    for row in datafilecsv:
        row.insert(0, course)
        row.insert(1, str(run))
        #print(row)
        datasetrows.append(row)
    
    return datasetrows

def download_course_dataset(b, file_path, course, dataset):

    # only write the header if this is a new download file
    write_header = True
    if os.path.exists(file_path):
        write_header = False

    # download the data until there is no runs left to download
    run = 1
    while True:
        try:
            datasetrows = get_dataset(b, course, run, dataset)

            # write the data to a file
            with open(file_path, "a", encoding='utf-8', newline="\n") as datafileoutput:
                writer = csv.writer(datafileoutput)
                
                # only take the header if its the first run
                startrow = 1
                if write_header:
                    startrow = 0
                    write_header = False
                writer.writerows(datasetrows[startrow:])

            print("- Run {}".format(run))

        except mechanicalsoup.LinkNotFoundError:
            if run == 1:
                raise DatasetNotFoundForCourse
            break

        run += 1

def download_data(courses=None, datasets=None, directory="."):
    
    b = login()

    # if a dataset is not provided, download for all datasets
    if datasets is None:
        datasets = DATASETS

    for dataset in datasets:
        if dataset in DATASETS:
            print("Dataset - {}".format(dataset))

            # create file path
            file_path = os.path.join(directory, "{}_{}.csv".format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"), dataset))
            print("Filename - {}".format(file_path))

            # delete any old files - belt and braces!
            if os.path.exists(file_path):
                print("- deleting old dataset")
                os.remove(file_path)

            # download the dataset for each course
            for course in courses:
                print("Course - {}".format(course))
                
                try:
                    download_course_dataset(b, file_path, course, dataset)

                except DatasetNotFoundForCourse:
                    print("Error: dataset [{}] was not found for course [{}].".format(dataset, course))
        else:
            raise DatasetNotKnownException()
