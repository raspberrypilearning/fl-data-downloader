from fl_data_downloader import FutureLearnData

fl = FutureLearnData(organisation="raspberry-pi")

# df = d.get_dataset_for_courses(courses=["introduction-to-databases-and-sql", "embedded-systems"], dataset="step_activity")
df = fl.get_dataset_for_courses(courses=["programming-101", "embedded-systems"], dataset="step_activity")

print(df)
