from fl_data_downloader import login, get_dataset

b = login()

courses = get_dataset(b, course="programming-101", run=2, dataset="enrolments")
print(courses)
