from .download import download_data, store_credentials, DATASETS, NeedToLoginException, DatasetNotKnownException, DatasetNotFoundForCourse

def main():
    from argparse import ArgumentParser

    parser = ArgumentParser(description="FutureLearn Data Downloader")
    parser.add_argument("course", nargs='+', help="The course(s) you want to download data for.")
    parser.add_argument("-d", "--dataset", nargs='+',  help="The dataset(s) you wish to download data for:\n {}".format(", ".join(DATASETS)))
    parser.add_argument("-o", "--output", help="The output directory where the data files should be written, defaults to the current directory.")
    parser.add_argument("-l", "--login", help="Login and store FutureLearn credentials.", action="store_true")
    args = parser.parse_args()
    
    if args.output:
        output_dir = args.output
    else:
        output_dir = "."

    if args.login:
        store_credentials()

    try:
        download_data(courses = args.course, datasets=args.dataset, directory=output_dir)

    except NeedToLoginException:
        print("Error: Dataset not returned? Is your username and password correct?\nReset stored credentials using [fl-data-dl course --login]")

    except DatasetNotKnownException:
        print("Error: [{}] is not a valid dataset. The options are:\n{}".format(args.dataset, ", ".join(DATASETS)))

    except KeyboardInterrupt:
        print("Cancelled")
