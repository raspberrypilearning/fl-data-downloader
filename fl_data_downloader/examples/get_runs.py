from fl_data_downloader import login, get_runs

b = login()

# get all runs of all courses
runs = get_runs(b, "raspberry-pi")

# or for a specific course
# runs = get_runs(b, "raspberry-pi", course="code-club")

print(runs)
