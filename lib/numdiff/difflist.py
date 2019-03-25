#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class for handling combining difflib.SequenceMatcher result merging.
"""
from __future__ import (
    division, print_function, absolute_import, unicode_literals)

__date__ = "2019/03/25 14:01:03 berhol"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2012 by Germanischer Lloyd SE, 2019 by DNV GL SE"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berthold.hoellmann@dnvgl.com"


class DiffList(object):
    """
>>> b = DiffList(maxchunk=2)
"""

    def __init__(self, maxchunk=20):
        self.vals = []
        self.maxchunk = maxchunk

    def append(self, val):
        """
>>> a = DiffList(maxchunk=5)
>>> a.append(('replace', 0, 3, 0, 3))
>>> a.append(('replace', 3, 5, 3, 5))
>>> a.append(('replace', 5, 9, 5, 9))
>>> a.vals == [('replace', 0, 5, 0, 5), ('replace', 5, 9, 5, 9)]
True
>>> a = DiffList()
>>> a.append(('equal', 0, 5, 0, 5))
>>> a.append(('replace', 5, 6, 5, 6))
>>> a.append(('equal', 6, 8, 6, 8))
>>> a.vals == [('equal', 0, 5, 0, 5), ('replace', 5, 6, 5, 6),
...     ('equal', 6, 8, 6, 8)]
True

"""
        if self.vals and self.vals[-1][0] == val[0]:
            if self.vals[-1][2] == val[1] and self.vals[-1][4] == val[3]:
                res = (self.vals[-1][0], self.vals[-1][1],
                       val[2], self.vals[-1][3], val[4])
                self.vals = self.vals[:-1]
            else:
                raise ValueError("Elements do not match: %s %s" %
                                 (self.vals[-1], val))
        else:
            res = val
        if self.vals and self.vals[0] is None:
            self.vals = [i for i in self.prepres(*res, maxchunk=self.maxchunk)]
        else:
            self.vals.extend(self.prepres(*res, maxchunk=self.maxchunk))

    @staticmethod
    def prepres(type, ai, aj, bi, bj, maxchunk):
        """
>>> DiffList.prepres('replace', 0, 5, 2, 7, 2) == [
...     ('replace', 0, 2, 2, 4), ('replace', 2, 4, 4, 6),
...      ('replace', 4, 5, 6, 7)]
True
>>> DiffList.prepres('replace', 0, 5, 2, 7, 2)[::-1] == [
...     ('replace', 4, 5, 6, 7), ('replace', 2, 4, 4, 6),
...     ('replace', 0, 2, 2, 4)]
True
>>> DiffList.prepres('A', 0, 5, 2, 7, 2) == (('A', 0, 5, 2, 7), )
True
"""
        if maxchunk is None or type != 'replace':
            return ((type, ai, aj, bi, bj), )
        _ai, _aj, _bi, _bj = ai, aj, bi, bj
        res = []
        while (_aj - _ai) > maxchunk:
            res.append((type, _ai, _ai+maxchunk, _bi, _bi+maxchunk),)
            _ai, _bi = _ai+maxchunk, _bi+maxchunk
        res.append((type, _ai, _aj, _bi, bj),)
        return res

    def extend(self, vals):
        """
>>> a = DiffList()
>>> a.extend([('equal', 0, 3, 0, 3), ('equal', 3, 5, 3, 5)])
>>> a.vals == [('equal', 0, 5, 0, 5)]
True
>>> a.extend([('replace', 5, 6, 5, 6), ('equal', 6, 8, 6, 8)])
>>> a.vals == [('equal', 0, 5, 0, 5), ('replace', 5, 6, 5, 6),
...         ('equal', 6, 8, 6, 8)]
True
"""
        [self.append(i) for i in vals]

    def __str__(self):
        """
>>> a = DiffList()
>>> a.extend((('equal', 0, 3, 0, 3), ('equal', 3, 5, 3, 5)))
>>> a.vals == [('equal', 0, 5, 0, 5)]
True
"""
        return str(self.vals)

    def __getitem__(self, i):
        """
>>> a = DiffList(maxchunk=2)
>>> a.extend((('replace', 0, 5, 0, 5), ))
>>> a[0] == ('replace', 0, 2, 0, 2)
True
"""
        return self.vals[i]

    def __setitem__(self, i, vals):
        """
>>> a = DiffList(maxchunk=2)
>>> a.extend((('replace', 0, 5, 0, 5), ))
>>> a[2] = ('A', 4, 5, 4, 5)
>>> a.vals == [('replace', 0, 2, 0, 2), ('replace', 2, 4, 2, 4),
...     ('A', 4, 5, 4, 5)]
True
"""
        self.vals[i] = vals

    def __len__(self):
        """
>>> print(len(DiffList.prepres('replace', 0, 5, 2, 7, 2)))
3
"""
        return len(self.vals)

# Local Variables:
# mode: python
# compile-command: "python ../../setup.py test"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
