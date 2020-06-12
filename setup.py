import sys
from setuptools import setup

if sys.version_info[0] == 2:
    raise ValueError('This package requires Python 3.5 or newer')
elif sys.version_info[0] == 3:
    if not sys.version_info >= (3, 5):
        raise ValueError('This package requires Python 3.5 or newer')
else:
    raise ValueError('Unrecognized major version of Python')

__project__ = "fl_data_downloader"
__package__ = "fl_data_downloader"
__version__ = '0.4.0'
__author__ = "Martin O'Hanlon"
__desc__ = 'A utility for downloading data set files for all runs of courses on FutureLearn'
__author_email__ = 'martin.ohanlon@raspberrypi.org'
__url__ = 'https://github.com/raspberrypilearning/fl-data-downloader'
__requires__ = ["MechanicalSoup", "pandas"]
__keywords__ = [
    "FutureLearn",
    "MOOC",
    "pandas",
]

__classifiers__ = [
#   "Development Status :: 3 - Alpha",
   "Development Status :: 4 - Beta",
#    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Intended Audience :: Developers",
    "Topic :: Education",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
]
__long_description__ = """# FutureLearn Data Downloader

The FutureLearn Data Downloader is a utility for accessing data about [FutureLearn](https://futurelearn.com) courses.

The API and download utility will download data for all runs of multiple courses, combining them together into a single dataset. 

It is useful for doing data analysis either in Python using [pandas](https://pandas.pydata.org/) or with csv files.

The [full documentation](https://fl-data-downloader.readthedocs.io/) describes how to install, its API and the download utility.
"""

if __name__ == '__main__':
    setup(
        name=__project__,
        version = __version__,
        description = __desc__,
        long_description=__long_description__,
        long_description_content_type='text/markdown',
        url = __url__,
        author = __author__,
        author_email = __author_email__,
        classifiers=__classifiers__,
        keywords=__keywords__,
        packages = [__package__],
        install_requires = __requires__,
        entry_points={
            'console_scripts': [
            'fl-data-dl = fl_data_downloader:fl_data_dl'
            ]},
        zip_safe=False)