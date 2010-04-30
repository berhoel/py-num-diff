#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Copyright (C) 2005 by Germanischer Lloyd AG

"""
$Header: /usr/local/gltools/cvsroot/src/numdiff/test.py,v 1.3 2007/12/12 14:34:09 hoel Exp $

======================================================================
Module    test
Task      test functionality for numdiff
----------------------------------------------------------------------
Author    Berthold Höllmann <hoel@GL-Group.com>
Project   numdiff
----------------------------------------------------------------------
Status    $State: Exp $
Date      $Date: 2007/12/12 14:34:09 $
======================================================================
"""

#  CVSID: $Id: test.py,v 1.3 2007/12/12 14:34:09 hoel Exp $
__author__       = ("2005 Germanischer Lloyd (author: $Author: hoel $) " +
                    "hoel@GL-Group.com")
__date__         = "$Date: 2007/12/12 14:34:09 $"
__version__      = "$Revision: 1.3 $"[10:-1]
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
            self.assertEqual(line1[0], line2)

class testRrList(unittest.TestCase):
    "testing RrList"

    def test1(self):
        "initial test"
        tester = numdiff.RrList(2)
        tester.append(1)
        tester.append(2)
        self.assertEqual(tester.list(), [1, 2])

    def test2(self):
        "testing maxlen ability"
        tester = numdiff.RrList(data=[1, 2, 3, 4, 5], maxlen=2)
        self.assertEqual(tester.list(), [4, 5])

    def test3(self):
        "testing maxlen with append"
        tester = numdiff.RrList(data=[1, 2, 3, 4, 5], maxlen=5)
        tester.append(6)
        self.assertEqual(tester.list(), [2, 3, 4, 5, 6])

class testNumDiff(unittest.TestCase):
    "Testing NumDiff class"

    def test1(self):
        "Testing for default comment lines"
        file1 = cStringIO.StringIO("""test
# hallo
got it?
""")
        file2 = cStringIO.StringIO("""test
got it?
""")
        tester = numdiff.NumDiff()
        self.assert_(tester.compare, (file1, file2))
        file1.close()
        file2.close()

    def test2(self):
        "testing for comment lines in real files"
        file1 = file('ref/first1.txt')
        file2 = file('ref/first2.txt')
        tester = numdiff.NumDiff()
        self.assert_(tester.compare, (file1, file2))
        file1.close()
        file2.close()

    def test3(self):
        "Don't ignore comment lines an check for thrown exception"
        file1 = file('ref/first1.txt')
        file2 = file('ref/first2.txt')
        tester = numdiff.NumDiff(options=dict(cchars=''))
        self.assertRaises(numdiff.NumDiffError, tester.compare, file1, file2)
        file1.close()
        file2.close()

    def test4(self):
        "Check for error with default eps"
        file1 = file('ref/second1.txt')
        file2 = file('ref/second2.txt')
        tester = numdiff.NumDiff()
        self.assertRaises(numdiff.NumDiffError, tester.compare, file1, file2)
        file1.close()
        file2.close()

    def test5(self):
        "Avoid error reporting with increased eps"
        file1 = file('ref/second1.txt')
        file2 = file('ref/second2.txt')
        tester = numdiff.NumDiff(options=dict(aeps=2e-5))
        self.assert_(tester.compare, (file1, file2))
        file1.close()
        file2.close()

    def test6(self):
        "Accept commas adjacent to values"
        file1 = file('ref/comma1.txt')
        file2 = file('ref/comma2.txt')
        tester = numdiff.NumDiff()
        self.assert_(tester.compare, (file1, file2))
        file1.close()
        file2.close()

if __name__ == '__main__':
    unittest.main()

# Local Variables:;
# compile-command:"python test.py";
# End:;

