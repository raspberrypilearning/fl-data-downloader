fl_data_downloader API
======================

.. module:: fl_data_downloader

The `fl_data_downloader` API can be used to gain and manipulate data using Python.

Data is returned as `pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_ objects. See the `pandas Getting started <https://pandas.pydata.org/pandas-docs/stable/getting_started/index.html>`_ for more information.

To use an API create a `FutureLearnData` object passing the organisation and call a `get_` method e.g.::

    from fl_data_downloader import FutureLearnData

    fl = FutureLearnData("raspberry-pi")

    dataset_df = fl.get_dataset_for_course(course="programming-101", dataset="enrolments")

    print(dataset_df)

There are code `examples <https://github.com/raspberrypilearning/fl-data-downloader/tree/master/fl_data_downloader/examples>`_ of how to use all the API calls in the `github repository <https://github.com/raspberrypilearning/fl-data-downloader>`_.

FutureLearnData
---------------

.. autoclass:: FutureLearnData

Credentials
-----------

.. automodule:: fl_data_downloader.credentials
   :members:
