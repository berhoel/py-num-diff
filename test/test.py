#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Copyright (C) 2005 by Germanischer Lloyd AG

"""
Module    test
Task      test functionality for numdiff
----------------------------------------------------------------------
Author    Berthold Höllmann <hoel@GL-Group.com>
Project   numdiff
"""

#  CVSID: $Id$
__author__ = ("2005 Germanischer Lloyd (author: $Author$) " +
              "hoel@GL-Group.com")
__date__ = "$Date$"
__version__ = "$Revision$"[10:-1]
__package_info__ = """ """

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

if __name__ == '__main__':

    doctest.set_unittest_reportflags(doctest.REPORT_CDIFF)
    SUITE = unittest.TestSuite()

    for mod in (numdiff, cmpline, difflist, files):
        SUITE.addTest(doctest.DocTestSuite(mod))

    RUNNER = unittest.TextTestRunner()
    RUNRES = RUNNER.run(SUITE)
    if RUNRES.errors or RUNRES.failures:
        raise Exception("failed test occured")

    unittest.main()

# Local Variables:
# compile-command:"python test.py"
# End:
