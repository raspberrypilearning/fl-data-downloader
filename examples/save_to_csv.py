from fl_data_downloader import FutureLearnData

fl = FutureLearnData(organisation="raspberry-pi")

# get the data
enrolments = fl.get_dataset(course="programming-101", run=1, dataset="enrolments")

enrolments.to_csv("my_dataset.csv")