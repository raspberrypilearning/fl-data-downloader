from fl_data_downloader import login, get_courses

b = login()

courses = get_courses(b, "raspberry-pi")
print(courses)
