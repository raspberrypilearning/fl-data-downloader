fl_data_downloader
==================

The `fl_data_downloader` API can be used to gain and manipulate data using Python.

To use an API you must call the `login()` function to gain a `b`rowser context which can be passed to `get_` functions e.g.::

    from fl_data_downloader import login, get_dataset_for_course

    b = login()

    dataset_df = get_dataset_for_course(b, course="programming-101", dataset="enrolments")

    print(dataset_df)

There are code `examples <https://github.com/raspberrypilearning/fl-data-downloader/tree/master/fl_data_downloader/examples>`_ of how to use all the API calls in the `github repository <https://github.com/raspberrypilearning/fl-data-downloader>`_.

Credentials
-----------

.. automodule:: fl_data_downloader.credentials
   :members:

Datasets
--------

.. automodule:: fl_data_downloader.datasets
   :members:

Courses
-------

.. automodule:: fl_data_downloader.courses
   :members:
   