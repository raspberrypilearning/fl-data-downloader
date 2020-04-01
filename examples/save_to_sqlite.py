import sqlite3
from fl_data_downloader import FutureLearnData

conn = sqlite3.connect("my_dataset.db")

fl = FutureLearnData(organisation="raspberry-pi")

df = fl.get_dataset_for_course(course="programming-101", dataset="enrolments")

df.to_sql("enrolments", conn, if_exists="replace")

conn.close()




