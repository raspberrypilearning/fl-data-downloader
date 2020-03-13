from fl_data_downloader import login, get_steps_for_run

b = login()

# get the steps for a single run for a single course
steps = get_steps_for_run(b, course="code-club", run=1)

print(steps)
