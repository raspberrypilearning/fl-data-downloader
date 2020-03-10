# FutureLearn Dataset Downloader

A utility for accessing datasets for [FutureLearn](https://futurelearn.com) courses.

The API and download utility will download data for all runs of multiple courses, combining them together into a single dataset. 

It is useful for doing data analysis either in Python using pandas or outside using `csv` files.

## What you need?

To use the dataset downloader utility you will need:
- Access to the internet
- [Python 3](https://www.python.org/downloads/) installed on your computer (be sure to click *Add Python to the PATH* when installing on Windows)
- [git](https://git-scm.com/downloads) installed on your computer
- a FutureLearn account which can access your courses dataset files

## Install

Open a command prompt or terminal and enter these commands:

```bash
git clone https://github.com/raspberrypilearning/fl-data-downloader
cd fl-data-downloader
pip3 install .
```

If you are installing on linux you may need to use `sudo` when running `pip3` in order to install the utiltiy.

```
sudo pip3 install .
```

If you are using Windows and you receive a `pip3 is not recognised` error, have a look at this guide to [Using pip on Windows](https://projects.raspberrypi.org/en/projects/using-pip-on-windows).


## Usage

### API

The `fl_data_downloader` uses [pandas](https://pandas.pydata.org/) and returns data as [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) objects. See the [pandas Getting started](https://pandas.pydata.org/pandas-docs/stable/getting_started/index.html) for more information.

To use an API you must call the `login()` function to gain a `b`rowser context which can be passed to `get_` functions e.g.

```python
from fl_data_downloader import login, get_dataset_for_course

b = login()

dataset_df = get_dataset_for_course(b, course="programming-101", dataset="enrolments")

print(dataset_df)
```

There are [examples](https://github.com/raspberrypilearning/fl-data-downloader/tree/meta_data/fl_data_downloader/examples) of how to use all the API calls.

### CSV download tool

The `fl-data-dl` command line tool can be used to download data for FutureLearn courses and datasets.

Each dataset is downloaded to a seperate file with the name `[yyyy-mm-dd-hh-mm-ss]-[dataset].csv`

Using the `-h` option will display the `fl-data-dl` command usage instructions.

```
fl-data-dl -h
```

```
usage: fl-data-dl [-h] [-d DATASET [DATASET ...]] [-o OUTPUT] [-l]
                  course [course ...]

FutureLearn Data Downloader

positional arguments:
  course                The course(s) you want to download data for.

optional arguments:
  -h, --help            show this help message and exit
  -d DATASET [DATASET ...], --dataset DATASET [DATASET ...]
                        The dataset(s) you wish to download data for:
                        archetype_survey_responses, campaigns, comments,
                        enrolments, leaving_survey_responses,
                        peer_review_assignments, peer_review_reviews,
                        post_course_survey_data, post_course_survey_free_text,
                        question_response, step_activity, team_members,
                        video_stats, weekly_sentiment_survey_responses
  -o OUTPUT, --output OUTPUT
                        The output directory where the data files should be
                        written, defaults to the current directory.
  -l, --login           Login and store FutureLearn credentials.
```

When the downloader is run, you will be asked to enter your FutureLearn username and password. 

See the examples below for help on using the tool for typical use cases.

## Examples

### Download all datasets for all runs of a course.

To download all the datasets for all the runs of the `programming-101` course:

```
fl-data-dl programming-101
```

### Download all datasets for multiple courses

Datasets for multiple courses can be combined by specifying a list of course names:

```
fl-data-dl programming-101 how-computers-work
```

### Download one specific dataset for a course

If you only need a specific dataset you can specify it using the `-d` option:

```
fl-data-dl programming-101 -d enrolments
```

### Specifying multiple datasets

Multiple datasets can also be provided:

```
fl-data-dl programming-101 -d enrolments campaigns
```

### Changing the output directory 

By default the data is saved to the current directory. You can change this using the `-o` option:

```
fl-data-dl programming-101 -o "c:\User\Martin OHanlon\Documents"
```

### Store login details password

You have to enter you FutureLearn username and password each time data is downloaded. You can store your login details by using the `--login` option.

```
fl-data-dl programming-101 --login
```

**Note:** the login configuration data is stored in `~/.fl-data-dl` (Linux, macOS) or `%USERPROFILE%\.fl-data-dl` (Windows) in plain text. If you are not confident your computer is secure you should not use this option.
