#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Copyright (C) 2005 by Germanischer Lloyd AG

"""
$Header: /data/tmp/hoel/tmp/cvstmp/numdiff/numdiff.py,v 1.3 2006-01-30 16:23:36 hoel Exp $

======================================================================
Module    numdiff
Task      numerical diff for text files
----------------------------------------------------------------------
Author    Berthold Höllmann <hoel@GL-Group.com>
Project   numdiff
----------------------------------------------------------------------
Status    $State: Exp $
Date      $Date: 2006-01-30 16:23:36 $
======================================================================
"""

#  CVSID: $Id: numdiff.py,v 1.3 2006-01-30 16:23:36 hoel Exp $
__author__       = ("2005 Germanischer Lloyd (author: $Author: hoel $) " +
                    "hoel@GL-Group.com")
__date__         = "$Date: 2006-01-30 16:23:36 $"
__version__      = "$Revision: 1.3 $"[10:-1]
__package_info__ = """ """

import copy
import re
import sys
from itertools import izip
from optparse import OptionParser

import Numeric as N

_float = re.compile(r"[-+]?(\d+(\.\d*)?|\d*\.\d+)([eE][-+]?\d+)?")
_int   = re.compile(r"[-+]?\d+(?![.eE])")

class NumDiffError(SystemExit):
    """Standard Error indicator for NumDiff
"""
    pass


class CFile(object):
    """Class for providing file information with ability to ignore
comment lines.
"""

    def __init__(self, fileObj, iscomment):
        self.fileObj = fileObj
        self.iscomment = iscomment
        self.line = 0

    def __iter__(self):
        for i in self.fileObj:
            self.line += 1
            if self.iscomment(i):
                continue
            yield i, self.line

class RrList(object):
    """Special list object that holds at most maxlen entries.
"""
    def __init__(self, maxlen, data=None):
        self.maxlen = maxlen
        if data is None:
            self.data = []
        else:
            self.data = data[-self.maxlen:]

    def append(self, item):
        """Append more data to the list and remove superfluous at the
beginning.
"""
        self.data = self.data[-self.maxlen+1:]
        self.data.append(item)

    def list(self):
        """Retrun copy of content.
"""
        return copy.copy(self.data)

    def clear(self):
        "empty data"
        self.data = []

class DiffContext(object):
    """Provides context information for diff reporting.
"""
    def __init__(self, lines=5, cline='', reportTo=sys.stderr):
        self.lines = lines
        self.cline = cline
        self.reportTo = reportTo
        self.current = RrList(lines)
        self.trailing = None

    def append(self, item1, item2=None):
        """Replace content.
"""
        if item2 is not None:
            self.trailing = 1
            self.report(item1[1], item1[0], item2)
        elif self.trailing is not None:
            self.reportTo.write('  %s' % (item1[0],))
            if self.trailing < self.lines:
                self.trailing += 1
            else:
                self.trailing = None
        else:
            self.current.append(item1[0])

    def report(self, line, item1, item2):
        "error report"
        list = self.current.list()
        if list or line == 1:
            self.reportTo.write('--- line %d ---\n' % (line-len(list), ))
            self.reportTo.write('%s' % ('  '.join(list)))
        self.reportTo.write('< %s' % (item1))
        self.reportTo.write('> %s' % (item2))
        self.current.clear()

class NumDiff(object):
    """Numerical diff for text files.
"""
    def __init__(self, cline='', options=None):
        if options is None:
            self.options = {}
        else:
            self.options = options
        self.aeps = self.options.get('aeps', 1e-8)
        self.reps = self.options.get('reps', 1e-5)
        self.context = DiffContext(self.options.get('context', 5),
                                   cline=cline)

    def iscomment(self, line):
        """is argument line a comment line?
"""
        return (bool(self.options.get('cchars', '#')) and
                line.startswith(self.options.get('cchars', '#')))

    def compare(self, fileA, fileB):
        """call the necessary methods
"""
        content1 = CFile(fileA, self.iscomment)
        content2 = CFile(fileB, self.iscomment)
        foundError = False
        for line1, line2 in izip(content1, content2):
            if line1[0] == line2[0]:
                self.context.append(line1)
            else:
                sLine1 = self.splitline(line1[0])
                sLine2 = self.splitline(line2[0])
                if len(sLine1) != len(sLine2):
                    self.context.append(line1, line2[0])
                    foundError = True
                    continue
                for token1, token2 in izip(sLine1, sLine2):
                    if token1 == token2:
                        continue
                    elif _float.match(token1) or _float.match(token2):
                        try:
                            if self.fequals(float(token1), float(token2)):
                                continue
                        except ValueError:
                            pass
                    elif _int.match(token1) or _int.match(token2):
                        if self.fequals(int(token1), int(token2)):
                            continue

                    self.context.append(line1, line2[0])
                    foundError = True
                    break
                else:
                    self.context.append(line1)
        if foundError:
            raise NumDiffError(1)


    @staticmethod
    def splitline(line):
        """Split line into tokens to be evaluated.
"""
        return line.split()

    def fequals(self, float1, float2):
        """Check for arguments beeing numerical equal.
"""
        return N.allclose(float1, float2, self.reps, self.aeps)

def main():
    """Main program. Used when called on command line.
"""
    doc = """\
usage: %prog [OPTIONS] FILE1 FILE2

Compare two text files with taking into account numerical errors.
"""
    parser = OptionParser(usage=doc)

    parser.add_option ("-c", "--comment-char",
                       action="store", type="string",
                       default=None,
                       metavar="<comment char>",
                       help="""Ignore lines starting with the comment
char when reading either file. Default: Do not ignore any line.""")
    parser.add_option ("-e", "--reps",
                       type="float", default=1e-5, metavar="<rEPS>",
                       help="""Relative error to be accepted in
numerial comparisons. Default: %default""")
    parser.add_option ("-a", "--aeps",
                       type="float", default=1e-8, metavar="<aEPS>",
                       help="""Relative error to be accepted in
numerial comparisons. Default: %default""")

    parser.add_option ("-C", "--context",
                       type="int", default="3", metavar="<LINES>",
                       help="""Number of context lines to be
reported. Default: %default""")

    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("incorrect number of arguments")

    file1 = file(args[0])
    file2 = file(args[1])
    worker = NumDiff(cline=" ".join(sys.argv),
                     options=dict(cchars=options.comment_char,
                                  aeps=options.aeps,
                                  reps=options.reps,
                                  context=options.context))
    worker.compare(file1, file2)
    file1.close()
    file2.close()

if __name__ == "__main__":
    main()

# Local Variables:;
# compile-command:"python setup.py build";
# End:;
