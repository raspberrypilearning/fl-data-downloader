from fl_data_downloader import login, get_courses

b = login()
# runs = get_runs(b, course="code-club")
# print(runs)
courses = get_courses(b)
print(courses)
