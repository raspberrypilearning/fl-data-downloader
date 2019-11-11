import mechanicalsoup
import configparser
import csv
import os

from datetime import datetime
from getpass import getpass

# exceptions
class NeedToLoginException(Exception):
    pass

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

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".fl-data-dl")

def get_credentials():
    # are there credentials in the config file?
    config = configparser.ConfigParser()
    
    config.read(CONFIG_PATH)

    user = config.get("fl", "user", fallback=None)
    pw = config.get("fl", "pw", fallback=None)

    # if not, ask for them
    if user is None or pw is None:
        user, pw = get_new_credentials()

    return user, pw

def get_new_credentials():
    print("Set your FutureLearn username and password")

    user = input("Username :")
    pw = getpass("Password :")

    return user, pw

def store_credentials():
    user, pw = get_new_credentials()

    config = configparser.ConfigParser()
    config.add_section("fl")
    config.set("fl", "user", user)
    config.set("fl", "pw", pw)

    # write new config gile
    with open(CONFIG_PATH, 'w') as configfile:
        config.write(configfile)

def login():
    user, pw = get_credentials()
    b = mechanicalsoup.StatefulBrowser(soup_config={'features':'lxml'}, raise_on_404=True, user_agent='Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',)
    b.open("https://www.futurelearn.com/sign-in")
    b.select_form('form[action="/sign-in"]')
    b["email"] = user
    b["password"] = pw
    response = b.submit_selected()
    return b

def get_dataset(b, course, run, dataset):

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
