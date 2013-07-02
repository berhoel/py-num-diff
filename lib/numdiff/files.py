#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
File identifier for numdiff.
"""

from __future__ import (print_function, division, absolute_import,
                        unicode_literals)

# ID: $Id$"
__date__ = "$Date$"[6:-1]
__version__ = "$Revision$"[10:-1]
__author__ = "`Berthold Höllmann <berthold.hoellmann@GL-group.com>`__"
__copyright__ = "Copyright © 2010 by Germanischer Lloyd SE"

import os.path

__all__ = ['fileFactory', 'RegularFile', 'Directory']


class NumDiffFileObject(object):
    """Base class for representing different file kinds.
"""
    def __init__(self, path, base):
        self.path = path
        self.base = base

    @property
    def name(self):
        """Returns filename (property)
"""
        return os.path.join(self.base, self.path)


class RegularFile(NumDiffFileObject):
    """
>>> a = RegularFile('2', '1')
>>> ('%s' % a) == ('%s is a regular file' % os.path.join('1', '2'))
True
"""
    def __str__(self):
        return "%s is a regular file" % os.path.join(self.base, self.path)


class EmptyFile(RegularFile):
    """
>>> a = EmptyFile('2', '1')
>>> ('%s' % a) == ('%s is a regular empty file' % os.path.join('1', '2'))
True
"""
    def __str__(self):
        return "%s is a regular empty file" % os.path.join(
            self.base, self.path)


class Directory(NumDiffFileObject):
    """
>>> a = Directory('2', '1')
>>> ('%s' % a) == ('%s is a directory' % os.path.join('1', '2'))
True
"""
    def __str__(self):
        return "%s is a directory" % os.path.join(self.base, self.path)


def fileFactory(path, base):
    """Factory method for generating apropriate instances of the
different subclasses of `NumDiffFileObject`.

>>> print('%s' % fileFactory('Makefile', ''))
Makefile is a regular file
>>> print('%s' % fileFactory('.', ''))
. is a directory
"""
    fname = os.path.join(base, path)
    statinfo = os.stat(fname)
    if os.path.isdir(fname):
        return Directory(path, base)
    elif statinfo.st_size == 0:
        return EmptyFile(path, base)
    return RegularFile(path, base)

# Local Variables:
# mode: python
# mode: flyspell
# ispell-local-dictionary: "en"
# compile-command: "make -C ../../test test"
# End:
