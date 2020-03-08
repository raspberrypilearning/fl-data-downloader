from fl_data_downloader import login, get_course_dataset

b = login()

courses = get_course_dataset(b, course="programming-101", dataset="enrolments")

print(courses)
