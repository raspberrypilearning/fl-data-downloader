from fl_data_downloader import FutureLearnData

fl = FutureLearnData(organisation="raspberry-pi")

df = fl.get_dataset_for_course(course="programming-101", dataset="step_activity")

print(df)
