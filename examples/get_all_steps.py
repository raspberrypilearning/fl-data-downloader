from fl_data_downloader import FutureLearnData

fl = FutureLearnData("raspberry-pi")

# get the steps for all the courses
df = fl.get_steps_for_courses()

# get the steps for a list of courses
# df = fl.get_steps_for_courses(courses=["embedded-systems", "programming-101"])

print(df)
