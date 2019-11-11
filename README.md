# FutureLearn Dataset Downloader

A utility for downloading datasets for FutureLearn courses.

It will download the data for all runs of a courses, combining them together into a single extract.

## Install

```bash
git clone https://github.com/raspberrypilearning/fl-data-dl
cd fl-data-dl
pip3 install .
```

## Usage

The `fl-data-dl` command line tool can be used to download data for FutureLearn courses and datasets.

Each dataset is downloaded to a seperate file with the name `[yyyy-mm-dd-hh-mm-ss]-[dataset].csv`

Using the `-h` will display the commands usage instructions.

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

### Download all datasets for a course.

To download all the datasets for all the runs of the `programming-101` course:

```
fl-data-dl programming-101
```

### Download a dataset for multiple courses

The datasets for multiple courses can be combined by specifying a list of course names:

```
fl-data-dl programming-101 how-computers-work
```

### Specify a dataset for a course

If you only need a specific dataset you can specify it using the `-d` option:

```
fl-data-dl programming-101 -d enrolments
```

### Get multiple datasets

Multiple datasets can also be provided:

```
fl-data-dl programming-101 enrolments campaigns
```

### Change the output directory 

By default the data is saved to the current directory. You can change this using the `-o` option:

```
fl-data-dl programming-101 -o "c:\User\Martin OHanlon\Documents"
```

### Store login details password

You have to enter you FutureLearn username and password each time data is downloaded. You can store your login details by using the `--login` option.

```
fl-data-dl programming-101 --login
```

**Note:** the configuration data is stored in `~/.fl-data-dl` (Linux, macOS) or `%USERPROFILE%\.fl-data-dl` (Windows) in plain text. If you are not confident your computer is secure you should not use this option.
