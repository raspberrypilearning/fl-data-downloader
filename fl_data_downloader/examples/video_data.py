from fl_data_downloader import login, get_courses, get_runs, get_dataset_for_course, get_dataset_for_courses, DATASETS

b = login()

courses_df = get_courses(b, "raspberry-pi")
# print(courses_df["course"].to_list())

# video_stats = get_dataset_for_course(b, "programming-101", "video_stats")
courses_list = ["computer-systems", "programming-101"]
video_stats = get_dataset_for_courses(b, courses_df["course"].to_list(), "video_stats")
# video_stats = get_dataset_for_courses(b, courses_list, "video_stats")

video_stats.to_csv("video_stats.csv")

print(video_stats)