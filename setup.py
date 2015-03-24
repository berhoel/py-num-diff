#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup file for numdiff.
"""

from __future__ import division, print_function, absolute_import

# Standard libraries.
from setuptools import setup

# ID: $Id$
__date__ = "$Date$"[6:-1]
__scm_version__ = "$Revision$"[10:-1]
__author__ = "`Berthold Höllmann <berthold.hoellmann@dnvgl.com>`__"
__copyright__ = "Copyright © 2013 by DNV GL SE"


if __name__ == '__main__':
    setup(name='numdiff',
          version='1.3',
          description="Numerical diff, written in Python",
          keywords="diff numerical compare",
          author='Berthold Höllmann',
          author_email="",
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
# ispell-local-dictionary: "english"
# compile-command: "python setup.py build"
# End:
