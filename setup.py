#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup file for numdiff.
"""

from __future__ import division, print_function, absolute_import

# Standard libraries.
from setuptools import setup

__date__ = "2019/03/25 14:10:25 berhol"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2013 by DNV GL SE, 2019 by DNV GL SE"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berthold.hoellmann@dnvgl.com"


if __name__ == '__main__':
    setup(name='numdiff',
          version='1.3.1',
          description="Numerical diff, written in Python",
          keywords="diff numerical compare",
          author='Berthold Höllmann',
          author_email="berthold.hoellmann@dnvgl.com",
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
# compile-command: "python ./setup.py test"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
