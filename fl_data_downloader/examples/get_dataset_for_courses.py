from fl_data_downloader import login, get_dataset_for_courses

b = login()

df = get_dataset_for_courses(b, courses=["introduction-to-databases-and-sql", "embedded-systems"], dataset="step_activity")

print(df)
