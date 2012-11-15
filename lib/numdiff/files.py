#! /usr/bin/env python
# -*- coding: utf-8 -*-

u"""
File identifier for numdiff

:author: `Berthold Hoellmann <hoel@GL-group.com>`__
:newfield project: Project
:project: numdiff
:copyright: Copyright (C) 2010 by Germanischer Lloyd AG"""

#  ID: $Id$
__date__ = u"$Date$"[5:-1]
__version__ = "$Revision$"[10:-1]
__docformat__ = "restructuredtext en"

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
>>> print '%s' % a
1/2 is a regular file
"""
    def __str__(self):
        return "%s is a regular file" % os.path.join(self.base, self.path)


class EmptyFile(RegularFile):
    """
>>> a = EmptyFile('2', '1')
>>> print '%s' % a
1/2 is a regular empty file
"""
    def __str__(self):
        return "%s is a regular empty file" % os.path.join(
            self.base, self.path)


class Directory(NumDiffFileObject):
    """
>>> a = Directory('2', '1')
>>> print '%s' % a
1/2 is a directory
"""
    def __str__(self):
        return "%s is a directory" % os.path.join(self.base, self.path)


def fileFactory(path, base):

    """Factory method for generating apropriate instances of the
different subclasses of `NumDiffFileObject`.

>>> print '%s' % fileFactory('Makefile', '')
Makefile is a regular file
>>> print '%s' % fileFactory('.', '')
. is a directory
>>> print '%s' % fileFactory('4', 'ref/1/')
ref/1/4 is a regular empty file
"""
    fname = os.path.join(base, path)
    statinfo = os.stat(fname)
    if os.path.isdir(fname):
        return Directory(path, base)
    elif statinfo.st_size == 0:
        return EmptyFile(path, base)
    return RegularFile(path, base)


def _test():
    """
run doctests
"""
    import doctest
    import importlib

    nlist = __name__.split('.')
    module = importlib.import_module(
        '.%s' % nlist[-1], '.'.join(nlist[:-1]))

    (failed, dummy) = doctest.testmod(module, verbose=True)
    if failed != 0:
        raise SystemExit(10)

# Local Variables:
# mode:python
# mode:flyspell
# ispell-local-dictionary:"en"
# compile-command:"make -C ../../test test"
# End:
