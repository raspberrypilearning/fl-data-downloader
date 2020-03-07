from fl_data_downloader import login, get_dataset

b = login()

courses = get_dataset(b, course="code-club", run=1, dataset="enrolments")
print(courses)
