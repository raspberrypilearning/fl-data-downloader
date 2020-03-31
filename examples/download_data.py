from fl_data_downloader import download_data

# single course, all datasets
files = download_data("raspberry-pi", ["programming-101"])

# multiple courses, all datasets
# files = download_data(["programming-101", "code-club"])

# single course, single dataset
# files = download_data(["programming-101"], ["enrolments"])

# single, multiple datasets
# files = download_data(["programming-101"], ["enrolments", "campaigns"])

print(files)