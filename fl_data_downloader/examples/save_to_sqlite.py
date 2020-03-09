import sqlite3
from fl_data_downloader import login, get_dataset_for_course

conn = sqlite3.connect("my_dataset.db")

b = login()

df = get_dataset_for_course(b, "raspberry-pi", course="programming-101", dataset="enrolments")
df.to_sql("enrolments", conn, if_exists="replace")

conn.close()