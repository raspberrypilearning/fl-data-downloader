from fl_data_downloader import login, get_dataset_for_course

b = login()

df = get_dataset_for_course(b, course="programming-101", dataset="enrolments")

print(df)
