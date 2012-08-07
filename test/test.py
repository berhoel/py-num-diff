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

import unittest
import cStringIO
from itertools import izip

import numdiff


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
    unittest.main()

# Local Variables:
# compile-command:"python test.py"
# End:
