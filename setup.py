#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Copyright (C) 2006 by Germanischer Lloyd AG

"""
======================================================================
Module    setup
Task      setup file for numdiff
----------------------------------------------------------------------
Author    Berthold Höllmann <hoel@GL-Group.com>
Project   numdiff
----------------------------------------------------------------------
Status    $State: Exp $
Date      $Date: 2006-01-16 15:02:35 $
======================================================================
"""

#  CVSID: $Id: setup.py,v 1.1.1.1 2006-01-16 15:02:35 hoel Exp $
__author__       = ("2006 Germanischer Lloyd (author: $Author: hoel $) " +
                    "hoel@GL-Group.com")
__date__         = "$Date: 2006-01-16 15:02:35 $"
__version__      = "$Revision: 1.1.1.1 $"[10:-1]
__package_info__ = """ """

from distutils.core import setup

setup(name='numdiff',
      version='1.0',
      description="Numrical diff, written in Python",
      author='B. Höllmann',
      author_email="hoel@GL-Group.com",
      py_modules=['numdiff'],
      scripts=['numdiff'],
      )

# Local Variables:;
# compile-command:"python setup.py build";
# End:;
