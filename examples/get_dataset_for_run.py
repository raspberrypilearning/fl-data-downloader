from fl_data_downloader import FutureLearnData

fl = FutureLearnData(organisation="raspberry-pi")

df = fl.get_dataset(course="programming-101", run=2, dataset="enrolments")
print(df)
