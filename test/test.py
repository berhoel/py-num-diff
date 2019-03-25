#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test functionality for numdiff.
"""

from __future__ import (
    division, print_function, absolute_import, unicode_literals)

# Standard libraries.
import sys
import doctest
import unittest

# DNV GL libraries.
import numdiff
from numdiff import files, cmpline, difflist

__date__ = "2019/03/25 14:15:41 berhol"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2005 by Germanischer Lloyd SE, 2019 DNV GL SE"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berthold.hoellmann@dnvgl.com"

if sys.version_info < (3, 1):
    from cStringIO import StringIO
else:
    from io import StringIO


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
        inp = StringIO("""test
! hallo
got it?
""")
        out = StringIO("""test
got it?
""")
        for line1, line2 in zip(numdiff.CFile(inp, self.iscomment), out):
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
# compile-command: "python ../setup.py test"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
