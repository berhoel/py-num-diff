#! /usr/bin/env python
# -*- coding: utf-8 -*-

u"""
setup file for numdiff

:author: `Berthold Hoellmann <hoel@GL-group.com>`__
:newfield project: Project
:project: numdiff
:copyright: Copyright (C) 2006 by Germanischer Lloyd AG
"""

# ID: $Id$
__date__ = u"$Date$"[5:-1]
__version__ = "$Revision$"[10:-1]
__docformat__ = "restructuredtext en"

import os.path
import re
from setuptools import setup
from distutils.command import build_scripts

build_scripts.first_line_re = re.compile(r'^###!.*python(\s+.*)?$')

setup(name='numdiff',
      version='1.1',
      description="Numerical diff, written in Python",
      keywords="diff numerical compare",
      author=u'Berthold Höllmann',
      author_email="hoel@GL-Group.com",
      license='Other/Proprietary License',
      package_dir={'': 'lib'},
      packages=['numdiff'],
      scripts=[os.path.join('app', 'numdiff')],
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Topic :: Utilities",
          "Environment :: Win32 (MS Windows)",
          "Environment :: Linux",
          "Intended Audience :: End Users/Desktop",
          "License :: Other/Proprietary License",
          "Topic :: Scientific/Engineering",]
      )

# Local Variables:
# mode:python
# mode:flyspell
# compile-command:"python setup.py build"
# End:
