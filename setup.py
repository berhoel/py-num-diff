#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup file for numdiff.
"""

# ID: $Id$"
__date__ = "$Date$"[6:-1]
__version__ = "$Revision$"[10:-1]
__author__ = "`Berthold Höllmann <berthold.hoellmann@GL-group.com>`__"
__copyright__ = "Copyright © 2013 by Germanischer Lloyd SE"

import re
from setuptools import setup
from distutils.command import build_scripts

build_scripts.first_line_re = re.compile(br'^###!.*python(\s+.*)?$')

if __name__ == '__main__':
    setup(name='numdiff',
          version='1.2',
          description="Numerical diff, written in Python",
          keywords="diff numerical compare",
          author='Berthold Höllmann',
          author_email="hoel@GL-Group.com",
          license='Other/Proprietary License',
          package_dir={'': 'lib'},
          packages=['numdiff'],
          entry_points={
              'console_scripts': [
                  'numdiff = numdiff:main']},
          classifiers=[
              "Development Status :: 5 - Production/Stable",
              "Topic :: Utilities",
              "Environment :: Win32 (MS Windows)",
              "Environment :: Linux",
              "Intended Audience :: End Users/Desktop",
              "License :: Other/Proprietary License",
              "Topic :: Scientific/Engineering"]
          )

# Local Variables:
# mode: python
# mode: flyspell
# ispell-local-dictionary: "en"
# compile-command: "python setup.py build"
# End:
