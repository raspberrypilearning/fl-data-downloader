from fl_data_downloader import login, get_dataset_for_courses

b = login()

df = get_dataset_for_courses(b, courses=["programming-101", "code-club"], dataset="enrolments")

print(df)
