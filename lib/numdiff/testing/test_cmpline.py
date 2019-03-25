#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Testing the numdiff.cmpline module.
"""
from __future__ import (
    division, print_function, absolute_import, unicode_literals)

# DNV GL libraries.
from numdiff.cmpline import CmpLine

__date__ = "2019/03/25 14:14:02 berhol"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2014 by Germanischer Lloyd SE, 2019 by DNV GL SE"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berthold.hoellmann@dnvgl.com"


class TestCmpLine(object):

    def test_compare_001(self):
        a = CmpLine("AA 1.00000000001")
        b = CmpLine("AA 1")
        c = CmpLine("BB")
        assert a != c
        assert a == b

# Local Variables:
# mode: python
# compile-command: "python ../../../setup.py test"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
