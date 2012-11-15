#! /usr/bin/env python
# -*- coding: utf-8 -*-

u"""
Class for handling combining difflib.SequenceMatcher result merging.

:author: `Berthold Hoellmann <hoel@GL-group.com>`__
:newfield project: Project
:project: numdiff
:copyright: Copyright (C) 2012 by Germanischer Lloyd SE
"""

# ID: $Id$
__date__ = u"$Date$"[6:-1]
__version__ = "$Revision$"[10:-1]
__docformat__ = "restructuredtext en"

class DiffList(object):
    """
>>> a = DiffList(('equal', 1, 3, 1, 3))
>>> a.append(('equal', 3, 5, 3, 5))
>>> print a
[('equal', 1, 5, 1, 5)]
>>> print a[0]
('equal', 1, 5, 1, 5)
"""
    def __init__(self, *vals):
        self.vals = []
        if vals:
            self.extend(vals)

    def append(self, val):
        if self.vals and self.vals[-1][0] == val[0]:
            if self.vals[-1][2] == val[1] and self.vals[-1][4] == val[3]:
                self.vals[-1] = (
                    self.vals[-1][0], self.vals[-1][1],
                    val[2], self.vals[-1][3], val[4])
            else:
                raise ValueError("Elements do not match: %s %s" %
                                 (self.vals[-1], val))
        else:
            self.vals.append(val)

    def extend(self, vals):
        [self.append(i) for i in vals]

    def __str__(self):
        return str(self.vals)

    def __getitem__(self, i):
        return self.vals[i]

    def __setitem__(self, i, vals):
        self.vals[i] = vals

    def __len__(self):
        return len(self.vals)

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
