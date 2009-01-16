#! /usr/bin/env python
# -*- coding: utf-8 -*-

u"""
numerical diff for text files

:author: `Berthold Höllmann <berthold.hoellmann@gl-group.com>`__
:newfield project: Project
:project: numdiff
:copyright: Copyright (C) 2005 by Germanischer Lloyd AG
"""

#  CVSID: $Id: numdiff.py,v 1.6 2008/07/03 07:41:32 hoel Exp $
__date__      = u"$Date: 2008/07/03 07:41:32 $"[5:-1]
__version__   = "$Revision: 1.6 $"[10:-1]
__docformat__ = "restructuredtext en"

import copy
import os
import os.path
import re
import sys
from itertools import izip
from optparse import OptionParser

import numpy as np

_float = re.compile(r"\s*[-+]?(\d+(\.\d*)?|\d*\.\d+)([eE][-+]?\d+)?\s*")
_int   = re.compile(r"\s*[-+]?\d+(?![.eE])\s*")

class NumDiffError(SystemExit):
    """Standard Error indicator for NumDiff
"""
    pass


class CFile(object):
    """Class for providing file information with ability to ignore
comment lines.
"""
    ws = re.compile("\s+")
    def __init__(self, fileObj, iscomment, ignore_space=False):
        self.fileObj = fileObj
        self.iscomment = iscomment
        self.ignore_space = ignore_space
        self.line = 0

    def __iter__(self):
        for i in self.fileObj:
            self.line += 1
            if self.iscomment(i):
                continue
            if self.ignore_space:
                yield " ".join(CFile.ws.split(i.strip())), i, self.line
            else:
                yield i, i, self.line

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
            if list:
                self.reportTo.write('  %s' % ('  '.join(list)))
        self.reportTo.write('< %s' % (item1))
        self.reportTo.write('> %s' % (item2))
        self.current.clear()

class NumDiff(object):
    """Numerical diff for text files.
"""
    linesplit = re.compile(r' *, *| +')
    def __init__(self, cline='', options=None):
        if options is None:
            self.options = {}
        else:
            self.options = options
        self.aeps = self.options.get('aeps', 1e-8)
        self.reps = self.options.get('reps', 1e-5)
        self.context = DiffContext(self.options.get('context', 5),
                                   cline=cline)
        if self.options.get('splitre') is not None:
            self.linesplit = re.compile(self.options['splitre'])
        self.ignore = None
        if self.options.get('ignore') is not None:
            self.ignore = re.compile(self.options['ignore'])

    def iscomment(self, line):
        """is argument line a comment line?
"""
        return (bool(self.options.get('cchars', '#')) and
                line.startswith(self.options.get('cchars', '#')))

    def compare(self, fileA, fileB):
        """call the necessary methods
"""
        content1 = iter(
            CFile(fileA, self.iscomment,
                  self.options.get("ignore_space", False)))
        content2 = iter(
            CFile(fileB,
                  self.iscomment, self.options.get("ignore_space", False)))
        foundError = False
        stopped1 = False
        while 1:
            try:
                line1 = content1.next()
            except StopIteration:
                stopped1 = True
            try:
                line2 = content2.next()
            except StopIteration:
                if stopped1:
                    break
                else:
                    raise NumDiffError('incompatible file length')
            if stopped1:
                raise NumDiffError('incompatible file length')
            if self.ignore is not None and self.ignore.search(line1[0]) and self.ignore.search(line2[0]):
                continue
            elif line1[0] == line2[0]:
                self.context.append(line1[1:])
            else:
                sLine1 = self.splitline(line1[0])
                sLine2 = self.splitline(line2[0])
                if len(sLine1) != len(sLine2):
                    self.context.append(line1[1:], line2[1])
                    foundError = True
                    continue
                for token1, token2 in izip(sLine1, sLine2):
                    if self.options.get("ignore_space", False):
                        token1 = token1.strip()
                        token2 = token2.strip()
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

                    self.context.append(line1[1:], line2[1])
                    foundError = True
                    break
                else:
                    self.context.append(line1[1:])
        if foundError:
            raise NumDiffError(1)


    def splitline(self, line):
        """Split line into tokens to be evaluated.
"""
        return self.linesplit.split(line)

    def fequals(self, float1, float2):
        """Check for arguments beeing numerical equal.
"""
        return np.allclose(float1, float2, self.reps, self.aeps)

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
    parser.add_option ("-b", "--ignore-space-change",
                       action="store_true",
                       help="""Ignore changes in the amount of
white space.""")
    parser.add_option ("-s", "--splitre",
                       type="str", default=None,
                       help="""python regular expression used to split
lines before checking for numerical changes""")
    parser.add_option ("-I", "--ignore-matching-lines", metavar="RE",
                       type="str", default=None,
                       help="""Ignore changes whose lines all match RE.""")
    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("incorrect number of arguments")

    file1 = file(args[0])
    if os.path.isdir(args[1]):
        file2 = file(os.path.join(args[1], os.path.split(args[0])[-1]))
    else:
        file2 = file(args[1])
    worker = NumDiff(cline=" ".join(sys.argv),
                     options=dict(cchars=options.comment_char,
                                  aeps=options.aeps,
                                  reps=options.reps,
                                  context=options.context,
                                  ignore_space=options.ignore_space_change,
                                  splitre=options.splitre,
                                  ignore=options.ignore_matching_lines))
    worker.compare(file1, file2)
    file1.close()
    file2.close()

if __name__ == "__main__":
    main()

# Local Variables:
# mode:python
# mode:flyspell
# compile-command:"make test"
# End:
