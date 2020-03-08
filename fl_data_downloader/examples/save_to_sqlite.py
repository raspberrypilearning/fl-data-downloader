import sqlite3
from fl_data_downloader import login, get_course_dataset

conn = sqlite3.connect("my_database.db")

b = login()

df = get_course_dataset(b, course="programming-101", dataset="enrolments")
df.to_sql("enrolments", conn, if_exists="replace")

conn.close()