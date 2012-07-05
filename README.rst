EVE Market Data Uploader (EMDU)
===============================

:Author: Greg Taylor
:License: BSD

This project contains a minimalistic EVE Online Market data uploader. It is
console-based, and aims to be the most cross-platform uploader.

Current state
-------------

Currently working reliably, just not configurable at all.

Source code is available on the `GitHub project`_.

.. _GitHub project: https://github.com/gtaylor/EVE-Market-Data-Uploader

Linux/Mac Install
-----------------

For the sake of simplicitly, these instructions install to system Python.
For those that car enough, use virtualenv. For everyone else who doesn't know
what that means, use these:

* Download the `latest source snapshot`_ from GitHub.
* Extract and ``cd`` to the extracted source.
* ``sudo pip install -r requirements.txt``
* ``sudo python setup.py install``
* You should now be able to run via ``emdu_console``

.. _latest source snapshot: https://github.com/gtaylor/EVE-Market-Data-Uploader/tarball/master

Windows Install
---------------

We'll eventually package this up more nicely, apologies for the hassle.

* Install Python 2.7 x86, x64 will not work due to incompatablities with
  reverence -- http://python.org/ftp/python/2.7.3/python-2.7.3.msi
* Install Reverence -- https://github.com/ntt/reverence/downloads
* Install Setuptools -- http://pypi.python.org/pypi/setuptools
* Download the `latest zipped source snapshot`_ from GitHub.
* Extract source, open shell, go to extraction location.
* Install software: ``python setup.py install``
* Test and run: ``python <python install path>\scripts\emdu_console``
* Optionally, add emdu_console to your path, which would let you just type
  ``emdu_console``.

.. _latest zipped source snapshot: https://github.com/gtaylor/EVE-Market-Data-Uploader/zipball/master

Specifying additional EVE directories
-------------------------------------

If EMDU's auto EVE installation detection doesn't work, you can append
additional EVE install dirs to search for cache directories. You can add
multiple EVE dirs by using the ``--add-eve`` flag multiple times::

    emdu_console --add-eve "/home/gtaylor/.wine/drive_c/users/gtaylor/Local Settings/Application Data/CCP/EVE/"

License
-------

This project, and all contributed code, are licensed under the BSD License.
A copy of the BSD License may be found in the repository.
