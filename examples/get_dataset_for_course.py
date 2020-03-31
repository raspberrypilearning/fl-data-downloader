from fl_data_downloader import FutureLearnData

fl = FutureLearnData(organisation="raspberry-pi", use_cache=False)

df = fl.get_dataset_for_course(course="programming-101", dataset="enrolments")

print(df)
