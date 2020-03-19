FutureLearn Data Downloader
==============================

The FutureLearn Data Downloader is a utility for accessing data about `FutureLearn <https://futurelearn.com>`_ courses.

The API and download utility will download data for all runs of multiple courses, combining them together into a single dataset. 

It is useful for doing data analysis either in Python using `pandas`_ or with `csv` files.

What you need?
--------------

To use the dataset downloader utility you will need:

+ Access to the internet
+ `Python 3 <https://www.python.org/downloads/>`_ installed on your computer (be sure to click *Add Python to the PATH* when installing on Windows)
+ `git <https://git-scm.com/downloads>`_ installed on your computer
+ a FutureLearn account which can access your courses dataset files

Install
-------

Open a command prompt or terminal and enter these commands::

    git clone https://github.com/raspberrypilearning/fl-data-downloader
    cd fl-data-downloader
    pip3 install .

If you are installing on linux you may need to use `sudo` when running `pip3` in order to install the utility::

    sudo pip3 install .

If you are using Windows and you receive a `pip3 is not recognised` error, have a look at this guide to `Using pip on Windows <https://projects.raspberrypi.org/en/projects/using-pip-on-windows>`_.

API
---

The `fl_data_downloader` returns data as `pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_ objects. See the `pandas Getting started <https://pandas.pydata.org/pandas-docs/stable/getting_started/index.html>`_ for more information.

To use an API you must call the `login()` function to gain a `b`rowser context which can be passed to `get_` functions e.g.::

    from fl_data_downloader import login, get_dataset_for_course

    b = login()

    dataset_df = get_dataset_for_course(b, course="programming-101", dataset="enrolments")

    print(dataset_df)

There are code `examples <https://github.com/raspberrypilearning/fl-data-downloader/tree/master/fl_data_downloader/examples>`_ of how to use all the API calls in the `github repository <https://github.com/raspberrypilearning/fl-data-downloader>`_.

CSV download tool
-----------------

The `fl-data-dl` command line tool can be used to download data for FutureLearn courses and datasets.

Each dataset is downloaded to a separate file with the name `[yyyy-mm-dd-hh-mm-ss]-[dataset].csv`

Using the `-h` option will display the `fl-data-dl` command usage instructions::

    fl-data-dl -h

::

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

e.g. to download all the datasets for all the runs of the `programming-101` course::

    fl-data-dl programming-101

When the downloader is run, you will be asked to enter your FutureLearn username and password. 

See the documentation for more details.

.. _pandas: https://pandas.pydata.org/