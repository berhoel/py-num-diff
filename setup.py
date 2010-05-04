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
__date__      = u"$Date$"[5:-1]
__version__   = "$Revision$"[10:-1]
__docformat__ = "restructuredtext en"

import os.path
import re
from distutils.core import setup
from distutils.command import build_scripts

build_scripts.first_line_re = re.compile(r'^###!.*python(\s+.*)?$')

setup(name='numdiff',
      version='1.1',
      description="Numrical diff, written in Python",
      author='B. Höllmann',
      author_email="hoel@GL-Group.com",
      package_dir={'': 'lib'},
      packages=['numdiff'],
      scripts=[os.path.join('app', 'numdiff')],
      )

# Local Variables:
# mode:python
# mode:flyspell
# compile-command:"python setup.py build"
# End:
