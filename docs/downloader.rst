fl-data-dl CSV downloader
=========================

The `fl-data-dl` command line tool can be used to download data for FutureLearn courses and datasets.

Each dataset is downloaded to a separate file with the name `[yyyy-mm-dd-hh-mm-ss]-[dataset].csv`

Using the `-h` option will display the `fl-data-dl` command usage instructions::

    fl-data-dl -h

::

    usage: fl-data-dl [-h] [-d DATASET [DATASET ...]] [-o OUTPUT] [-l] [-v] organisation course [course ...]

    FutureLearn Data Downloader

    positional arguments:
    organisation          The organisation you want to download data for.
    course                The course(s) you want to download data for.

    optional arguments:
    -h, --help            show this help message and exit
    -d DATASET [DATASET ...], --dataset DATASET [DATASET ...]
                            The dataset(s) you wish to download data for: archetype_survey_responses, campaigns, comments, enrolments,
                            leaving_survey_responses, peer_review_assignments, peer_review_reviews, post_course_survey_data,
                            post_course_survey_free_text, question_response, step_activity, team_members, video_stats,
                            weekly_sentiment_survey_responses
    -o OUTPUT, --output OUTPUT
                            The output directory where the data files should be written, defaults to the current directory.
    -l, --login           Login and store FutureLearn credentials.
    -v, --version         Display the version number

When the downloader is run, you will be asked to enter your FutureLearn username and password. 

See the examples below for help on using the tool for typical use cases.

Examples
--------

**Download all datasets for all runs of a course**

To download all the datasets for all the runs of the `programming-101` course for the `raspberry-pi` organisation::

    fl-data-dl raspberry-pi programming-101

**Download all datasets for multiple courses**

Datasets for multiple courses can be combined by specifying a list of course names::

    fl-data-dl raspberry-pi programming-101 how-computers-work

**Download one specific dataset for a course**

If you only need a specific dataset you can specify it using the `-d` option::

    fl-data-dl raspberry-pi programming-101 -d enrolments

**Specifying multiple datasets**

Multiple datasets can also be provided::

    fl-data-dl raspberry-pi programming-101 -d enrolments campaigns

**Changing the output directory**

By default the data is saved to the current directory. You can change this using the `-o` option::

    fl-data-dl raspberry-pi programming-101 -o "c:\User\Martin OHanlon\Documents"

**Store login details password**

You have to enter you FutureLearn username and password each time data is downloaded. You can store your login details by using the `--login` option::

    fl-data-dl raspberry-pi programming-101 --login

*Note:* the login configuration data is stored in `~/.fl-data-dl` (Linux, macOS) or `%USERPROFILE%\.fl-data-dl` (Windows) in plain text. If you are not confident your computer is secure you should not use this option.
