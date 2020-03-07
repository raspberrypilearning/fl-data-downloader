from fl_data_downloader import login, get_run_steps

b = login()

steps = get_run_steps(b, course="code-club", run=1)
print(steps)

