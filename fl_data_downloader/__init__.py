from .credentials import (
    login, 
    store_credentials
    )

from .data import (
    FutureLearnData,
    download_data,
    AVAILABLE_DATASETS
)

from .exceptions import (
    NeedToLoginException, 
    DatasetNotKnownException, 
    DatasetNotFoundForCourse,
    CourseRunNotFound
    )

def fl_data_dl():

    from argparse import ArgumentParser

    parser = ArgumentParser(description="FutureLearn Data Downloader")
    parser.add_argument("organisation", help="The organisation you want to download data for.")
    parser.add_argument("course", nargs='+', help="The course(s) you want to download data for.")
    parser.add_argument("-d", "--dataset", nargs='+',  help="The dataset(s) you wish to download data for:\n {}".format(", ".join(AVAILABLE_DATASETS)))
    parser.add_argument("-o", "--output", help="The output directory where the data files should be written, defaults to the current directory.")
    parser.add_argument("-l", "--login", help="Login and store FutureLearn credentials.", action="store_true")
    parser.add_argument("-V", "--version", help="Display the version number.", action="version", version="fl_data_downloader (0.4.0)")
    parser.add_argument("--no-cache", help="Disable the cache.", action="store_true")
    args = parser.parse_args()
    
    if args.output:
        output_dir = args.output
    else:
        output_dir = "."

    if args.login:
        store_credentials()

    try:
        download_data(organisation=args.organisation, courses=args.course, datasets=args.dataset, directory=output_dir, use_cache=not args.no_cache)

    except NeedToLoginException:
        print("Error: Dataset not returned? Is your username and password correct?\nReset stored credentials using [fl-data-dl course --login]")

    except DatasetNotKnownException:
        print("Error: [{}] is not a valid dataset. The options are:\n{}".format(args.dataset, ", ".join(AVAILABLE_DATASETS)))

    except KeyboardInterrupt:
        print("Cancelled")
