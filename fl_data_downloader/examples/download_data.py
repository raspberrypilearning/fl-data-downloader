from fl_data_downloader import download_data

# single course, all datasets
download_data(["programming-101"])

# multiple courses, all datasets
# download_data(["programming-101", "code-club"])

# single course, single dataset
# download_data(["programming-101"], ["enrolments"])

# single, multiple datasets
# download_data(["programming-101"], ["enrolments", "campaigns"])

