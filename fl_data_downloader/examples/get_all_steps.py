from fl_data_downloader import login, get_steps_for_courses

b = login()

# get the steps for a list of course
steps = get_steps_for_courses(b, "raspberry-pi", courses=["embedded-systems", "programming-101"])

# get the steps for all the courses
steps = get_steps_for_courses(b, "raspberry-pi")

print(steps)
