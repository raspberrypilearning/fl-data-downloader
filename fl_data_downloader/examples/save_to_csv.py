from fl_data_downloader import login, get_dataset

b = login()

# get the data
courses = get_dataset(b, course="programming-101", run=1, dataset="enrolments")

courses.to_csv("my_dataset.csv")