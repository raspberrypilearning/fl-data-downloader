"""
Generate a SQLite database of all the dataset data from all the courses for an organisation
"""

import os
import sqlite3

from fl_data_downloader import FutureLearnData, AVAILABLE_DATASETS, DatasetNotFoundForCourse

db_file = "all_courses.db"

if os.path.exists(db_file):
    print("Deleting old database")
    os.remove(db_file)

conn = sqlite3.connect(db_file)

# create data objects
fl = FutureLearnData("raspberry-pi")

# get the courses
courses_df = fl.get_courses()

# get a list of all the course names
courses = list(courses_df["course"].sort_values().to_list())

# for each course download all the datasets and append to tables
count = 0
for course in courses: 
    count += 1
    print("{} - {} of {}".format(course, count, len(courses)))

    for dataset in AVAILABLE_DATASETS:
        print(dataset)
        try:
            df = fl.get_dataset_for_course(course=course, dataset=dataset)
            if df is not None:
                df.to_sql(dataset, conn, if_exists="append")

        except DatasetNotFoundForCourse:
            print("- dataset not found")
        
conn.close()