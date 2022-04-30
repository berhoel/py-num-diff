#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
File identifier for numdiff.
"""

# Standard libraries.
import os.path

__date__ = "2022/04/30 19:09:08 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2010 by Germanischer Lloyd SE, 2019 by DNV GL SE"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berthold.hoellmann@dnvgl.com"


__all__ = ["fileFactory", "RegularFile", "Directory"]


class NumDiffFileObject(object):
    """Base class for representing different file kinds."""

    def __init__(self, path, base):
        self.path = path
        self.base = base

    @property
    def name(self):
        """Returns filename (property)"""
        return os.path.join(self.base, self.path)


class RegularFile(NumDiffFileObject):
    """
    >>> a = RegularFile('2', '1')
    >>> ('%s' % a) == ('%s is a regular file' % os.path.join('1', '2'))
    True"""

    def __str__(self):
        return "%s is a regular file" % os.path.join(self.base, self.path)


class EmptyFile(RegularFile):
    """
    >>> a = EmptyFile('2', '1')
    >>> ('%s' % a) == ('%s is a regular empty file' % os.path.join('1', '2'))
    True"""

    def __str__(self):
        return "%s is a regular empty file" % os.path.join(self.base, self.path)


class Directory(NumDiffFileObject):
    """
    >>> a = Directory('2', '1')
    >>> ('%s' % a) == ('%s is a directory' % os.path.join('1', '2'))
    True"""

    def __str__(self):
        return "%s is a directory" % os.path.join(self.base, self.path)


def fileFactory(path, base):
    """Factory method for generating apropriate instances of the
    different subclasses of `NumDiffFileObject`.

    >>> print('%s' % fileFactory('Makefile', ''))
    Makefile is a regular file
    >>> print('%s' % fileFactory('.', ''))
    . is a directory"""
    fname = os.path.join(base, path)
    statinfo = os.stat(fname)
    if os.path.isdir(fname):
        return Directory(path, base)
    elif statinfo.st_size == 0:
        return EmptyFile(path, base)
    return RegularFile(path, base)


# Local Variables:
# mode: python
# compile-command: "python ../../setup.py test"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
