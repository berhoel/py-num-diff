#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test functionality for numdiff.
"""

from __future__ import (print_function, division, absolute_import,
                        unicode_literals)

# ID: $Id$"
__date__ = "$Date$"[6:-1]
__version__ = "$Revision$"[10:-1]
__author__ = "`Berthold Höllmann <berthold.hoellmann@GL-group.com>`__"
__copyright__ = "Copyright © 2005 by Germanischer Lloyd SE"

import doctest
import unittest
import cStringIO
from itertools import izip

import numdiff
from numdiff import cmpline, difflist, files


class testCfile(unittest.TestCase):
    """Test method for class CFile.
"""
    @staticmethod
    def iscomment(line):
        """Check for comment lines.
"""
        return line.startswith('!')

    def test1(self):
        """First test.
"""
        inp = cStringIO.StringIO("""test
! hallo
got it?
""")
        out = cStringIO.StringIO("""test
got it?
""")
        for line1, line2 in izip(numdiff.CFile(inp, self.iscomment), out):
            self.assertEqual(line1, line2)


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(numdiff))
    tests.addTests(doctest.DocTestSuite(cmpline))
    tests.addTests(doctest.DocTestSuite(difflist))
    tests.addTests(doctest.DocTestSuite(files))
    return tests


if __name__ == '__main__':
    unittest.main()

# Local Variables:
# mode: python
# mode: flyspell
# ispell-local-dictionary: "en"
# compile-command: "python test.py"
# End:
