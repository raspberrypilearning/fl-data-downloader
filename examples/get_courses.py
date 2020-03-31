from fl_data_downloader import FutureLearnData

c = FutureLearnData("raspberry-pi")

df = c.get_courses()

print(df)
