from fl_data_downloader import login, get_dataset

b = login()

df = get_dataset(b, course="programming-101", run=2, dataset="step_activity")
print(df)
