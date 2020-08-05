from fl_data_downloader import FutureLearnData

c = FutureLearnData("raspberry-pi", use_cache=False)

df = c.get_courses()

print(df)
