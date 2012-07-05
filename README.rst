EVE Market Data Uploader (EMDU)
===============================

:Author: Greg Taylor
:License: BSD

This project contains a minimalistic EVE Online Market data uploader. It is
console-based, and aims to be the most cross-platform uploader.

Current state
-------------

I'm tinkering with it when I feel like it. This may or may never see the
light of day, but it's a fun toy.

Linux/Mac Install
-----------------

* ``pip install -r requirements.txt``
* ``python setup.py install``
* You should now be able to run via ``emdu_console``

Windows Install
---------------

We'll eventually package this up more nicely, apologies for the hassle.

* Install Python 2.7 x86, x64 will not work due to incompatablities with
  reverence -- http://python.org/ftp/python/2.7.3/python-2.7.3.msi
* Install Reverence -- https://github.com/ntt/reverence/downloads -- https://github.com/downloads/ntt/reverence/reverence-1.4.2.win32-py2.7.exe
* Install Setuptools -- http://pypi.python.org/pypi/setuptools -- http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11.win32-py2.7.exe
* Download source of the EMDU from github -- https://github.com/gtaylor/EVE-Market-Data-Uploader/tree/win32 -- https://github.com/gtaylor/EVE-Market-Data-Uploader/zipball/master
* Extract source, open shell, goto extraction location
* Install software: ``python setup.py install``
* Test and run: ``python <python install path>\scripts\emdu_console``
* Optionally, add emdu_console to your path, which would let you just type
  ``emdu_console``.

License
-------

This project, and all contributed code, are licensed under the BSD License.
A copy of the BSD License may be found in the repository.
