Developers
==========

Contributions are very welcome; be that changes, bug fixing, issue resolution or support.

All issues should be raise on `github.com/raspberrypilearning/fl-data-downloader/issues <https://github.com/raspberrypilearning/fl-data-downloader/issues>`_

When providing code changes please:

 * use the dev branch as the base for all changes
 * create a single pull requests for each fix / addition
 * follow the existing coding style
 * provide documentation for all changes as rst in /docs

These are instructions for how to develop, build and deploy fl-data-downloader.

Install
-------

Install / upgrade tools::

    python -m pip install --upgrade pip setuptools wheel twine 

Clone repo and install for dev::

    git clone https://github.com/raspberrypilearning/fl-data-downloader
    cd fl-data-downloader
    git checkout dev
    python setup.py develop

Deploy
------

Update version numbers::
    setup.py
    fl_data_downloader/__init__.py
    docs/changelog.rst

Build for deployment::

    python setup.py sdist
    python setup.py bdist_wheel
    
Deploy to `PyPI`_::

    twine upload dist/* --skip-existing

.. _PyPI: https://pypi.python.org/pypi