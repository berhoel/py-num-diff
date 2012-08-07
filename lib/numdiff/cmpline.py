#! /usr/bin/env python
# -*- coding: utf-8 -*-

u"""
Class for alowing numerical diffing of text lines.

:author: `Berthold Hoellmann <hoel@GL-group.com>`__
:newfield project: Project
:project: numdiff
:copyright: Copyright (C) 2010 by Germanischer Lloyd AG"""

#  ID: $Id$
__date__ = u"$Date$"[5:-1]
__version__ = "$Revision$"[10:-1]
__docformat__ = "restructuredtext en"

from itertools import izip
import re

import numpy as np

_FLOAT = re.compile(r"\s*[-+]?(\d+(\.\d*)?|\d*\.\d+)([eE][-+]?\d+)?\s*")
_INT = re.compile(r"\s*[-+]?\d+(?![.eE])\s*")


class CmpLine(object):
    """Representing test lines to be compared.

Tries literal comparison of lines first. If this fails, tries
numerical comparison.
"""

    linesplit = re.compile(r' *, *| +')

    def __init__(self, line, options=None):
        self.line = line
        if options is None:
            self.options = {}
        else:
            self.options = options
        self.value = self.line
        if self.options.get('ignore_space_change'):
            self.value = self.value.strip()
        self.ignore = None
        if self.options.get('ignore') is not None:
            self.ignore = re.compile(self.options['ignore'])
        if self.options.get('splitre') is not None:
            self.linesplit = re.compile(self.options['splitre'])
        self.aeps = self.options.get('aeps', 1e-8)
        self.reps = self.options.get('reps', 1e-5)

    def __cmp__(self, other):
        if (self.ignore is not None and
            self.ignore.search(self.value) and
            self.ignore.search(other.value)):
            return 0
        elif self.value == other.value:
            return 0
        else:
            sLine1 = self.splitline(self.value)
            sLine2 = self.splitline(other.value)
            if len(sLine1) != len(sLine2):
                return 1
            for token1, token2 in izip(sLine1, sLine2):
                if self.options.get("ignore_space", False):
                    token1 = token1.strip()
                    token2 = token2.strip()
                if token1 == token2:
                    continue
                elif _FLOAT.match(token1) or _FLOAT.match(token2):
                    try:
                        if self.fequals(float(token1), float(token2)):
                            continue
                    except ValueError:
                        pass
                elif _INT.match(token1) or _INT.match(token2):
                    if self.fequals(int(token1), int(token2)):
                        continue

                return 1
            return 0

    def fequals(self, float1, float2):
        """Check for arguments beeing numerical equal.
"""
        return np.allclose(float1, float2, self.reps, self.aeps)

    def splitline(self, line):
        """Split line into tokens to be evaluated.
"""
        return self.linesplit.split(line)

    def __str__(self):
        return self.line

    def __radd__(self, other):
        return other + self.value

    def __len__(self):
        return len(self.value)

    def __getitem__(self, item):
        return self.value[item]

    def __hash__(self):
        return hash(self.value)


def _test():
    """
run doctests
"""
    import doctest

    module = __import__(__name__)

    (failed, dummy) = doctest.testmod(module, verbose=True)
    if failed != 0:
        raise SystemExit(10)

# Local Variables:
# mode:python
# mode:flyspell
# compile-command:"make -C ../../test test"
# End:
