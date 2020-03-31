from fl_data_downloader import FutureLearnData

fl = FutureLearnData("raspberry-pi")

status = fl.get_run_active_status("programming-101", 1)
status = fl.get_run_active_status("programming-101", 6)

print(status)
