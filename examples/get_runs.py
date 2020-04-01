from fl_data_downloader import FutureLearnData

fl = FutureLearnData("raspberry-pi")

df = fl.get_runs()

print(df)
