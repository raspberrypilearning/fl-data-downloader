import sys
from setuptools import setup
from fl_data_downloader import __name__, __package__, __version__, __author__

if sys.version_info[0] == 2:
    raise ValueError('This package requires Python 3.5 or newer')
elif sys.version_info[0] == 3:
    if not sys.version_info >= (3, 5):
        raise ValueError('This package requires Python 3.5 or newer')
else:
    raise ValueError('Unrecognized major version of Python')

__desc__ = 'A utility for downloading data set files for all runs of courses on FutureLearn'
__author_email__ = 'martin.ohanlon@raspberrypi.org'
__url__ = 'https://github.com/raspberrypilearning/fl_data_downloader'
__requires__ = ["MechanicalSoup", "pandas"]

if __name__ == '__main__':
    setup(
        name=__name__,
        version = __version__,
        description = __desc__,
        url = __url__,
        author = __author__,
        author_email = __author_email__,
        packages = [__package__],
        install_requires = __requires__,
        entry_points={
            'console_scripts': [
            'fl-data-dl = fl_data_downloader:main'
            ]},
        zip_safe=False)