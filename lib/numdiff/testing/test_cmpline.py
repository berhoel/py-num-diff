#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Testing the numdiff.cmpline module.
"""

from __future__ import (print_function, division, absolute_import,
                        unicode_literals)

# ID: $Id$"
__date__ = "$Date$"[6:-1]
__version__ = "$Revision$"[10:-1]
__author__ = "`Berthold Höllmann <berthold.hoellmann@GL-group.com>`__"
__copyright__ = "Copyright © 2014 by Germanischer Lloyd SE"

from ..cmpline import CmpLine


class TestCmpLine(object):

    def test_compare_001(self):
        a = CmpLine("AA 1.00000000001")
        b = CmpLine("AA 1")
        c = CmpLine("BB")
        assert a != c
        assert a == b

# Local Variables:
# mode: python
# ispell-local-dictionary: "english"
# compile-command: "python setup.py build"
# End:
