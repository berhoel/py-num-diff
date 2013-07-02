#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class for alowing numerical diffing of text lines.
"""

from __future__ import (print_function, division, absolute_import,
                        unicode_literals)

# ID: $Id$"
__date__ = "$Date$"[6:-1]
__version__ = "$Revision$"[10:-1]
__author__ = "`Berthold Höllmann <berthold.hoellmann@GL-group.com>`__"
__copyright__ = "Copyright © 2010 by Germanischer Lloyd SE"

import re

__all__ = ['CmpLine']

_FLOAT = re.compile(r"\s*[-+]?(\d+(\.\d*)?|\d*\.\d+)([eE][-+]?\d+)?\s*")
_INT = re.compile(r"\s*[-+]?\d+(?![.eE])\s*")


class CmpLine(object):
    """Representing test lines to be compared.

Tries literal comparison of lines first. If this fails, tries
numerical comparison.

>>> a, b, c = CmpLine("AA 1.00000000001"), CmpLine("AA 1"), CmpLine("BB")
>>> a == c
False
>>> a == b
True
"""

    linesplit = re.compile(r' *, *| +')

    def __init__(self, line, options=None):
        self.line = line
        if options is None:
            self.options = {'fixcols': None}
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

    def __eq__(self, other):
        if self.options.get('verbose'):
            print("__EQ__ !%s! !%s!" % (self.value.split('\n')[0],
                                        other.value.split('\n')[0]))
        if self.ignore is not None and self.ignore.search(self.value) and \
          self.ignore.search(other.value):
            if self.options.get('verbose'):
                print("IGNORE !%s! !%s!" % (self.value.split('\n')[0],
                                            other.value.split('\n')[0]))
            return True
        elif self.value.split('\n')[0] == other.value.split('\n')[0]:
            if self.options.get('verbose'):
                print("EQUAL !%s! !%s!" % (self.value.split('\n')[0],
                                           other.value.split('\n')[0]))
            return True
        else:
            sLine1 = self.splitline(self.value.split('\n')[0])
            sLine2 = self.splitline(other.value.split('\n')[0])
            if len(sLine1) != len(sLine2):
                if self.options.get('verbose'):
                    print("SPLITLEN !%s! !%s!" % (
                        self.value.split('\n')[0], other.value.split('\n')[0]))
                return False
            for token1, token2 in zip(sLine1, sLine2):
                if self.options.get('verbose'):
                    print('token1: ', token1, '; token2: ', token2)
                if self.options.get("ignore_space", False):
                    token1 = token1.strip()
                    token2 = token2.strip()
                if token1 == token2:
                    continue
                elif _FLOAT.match(token1) or _FLOAT.match(token2):
                    if self.options.get('verbose'):
                        print("FLOAT !%s! !%s!" % (self.value.split('\n')[0],
                                                   other.value.split('\n')[0]))
                    try:
                        if self.fequals(float(token1), float(token2)):
                            continue
                    except ValueError:
                        if self.options.get('verbose'):
                            print("ValueError !%s! !%s!" % (
                                self.value.split('\n')[0],
                                other.value.split('\n')[0]))
                elif _INT.match(token1) or _INT.match(token2):
                    if self.options.get('verbose'):
                        print("INT !%s! !%s!" % (self.value.split('\n')[0],
                                                 other.value.split('\n')[0]))
                    if self.fequals(int(token1), int(token2)):
                        continue

                if self.options.get('verbose'):
                    print("TOKEN !%s! !%s!" % (
                        self.value.split('\n')[0], other.value.split('\n')[0]))
                return False
            if self.options.get('verbose'):
                print("SAME !%s! !%s!" % (
                    self.value.split('\n')[0], other.value.split('\n')[0]))
            return True

    def fequals(self, float1, float2):
        """Check for arguments beeing numerical equal.
"""
        if self.options.get('verbose'):
            print("fequals: ", float1, float2,
                  abs(float1 - float2), (self.aeps + self.reps * abs(float2)))

        return abs(float1 - float2) <= (self.aeps + self.reps * abs(float2))

    def splitline(self, line):
        """Split line into tokens to be evaluated.
"""
        if self.options['fixcols']:
            return [line[i:j] for i, j in zip([0] +
                    self.options['fixcols'][:-1],
                    self.options['fixcols'])]
        else:
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
        return 1

# Local Variables:
# mode: python
# mode: flyspell
# ispell-local-dictionary: "en"
# compile-command: "make -C ../../test test"
# End:
