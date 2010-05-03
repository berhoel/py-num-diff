#! /usr/bin/env python
# -*- coding: utf-8 -*-

u"""
numerical diff for text files

:author: `Berthold Höllmann <berthold.hoellmann@gl-group.com>`__
:newfield project: Project
:project: numdiff
:copyright: Copyright (C) 2005 by Germanischer Lloyd AG
"""

from __future__ import absolute_import

import copy
import difflib
import glob
import os
import os.path
import re
import sys
from itertools import izip, chain, repeat
from optparse import OptionParser, make_option

import numpy as np

from .files import fileFactory, RegularFile
from .cmpline import CmpLine

#  CVSID: $Id$
__date__      = u"$Date$"[5:-1]
__version__   = "$Revision$"[10:-1]
__docformat__ = "restructuredtext en"

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
                yield " ".join(CFile.ws.split(i.strip()))#, i, self.line
            else:
                yield i#, i, self.line

class Main():
    """Main program. Used when called on command line.
"""
    DOC = """\
usage: %prog [OPTIONS] FILE1 FILE2

Compare two text files with taking into account numerical errors.
"""
    def __init__(self):
        self.options = None
        self.args = None
        self.optdict = {}

    def __call__(self):
        self.parse_cmdline()
        self.optdict.update(
            dict(cchars=self.options.comment_char,
                 aeps=self.options.aeps,
                 reps=self.options.reps,
                 context=self.options.context,
                 ignore_space=self.options.ignore_space_change,
                 splitre=self.options.splitre,
                 ignore=self.options.ignore_matching_lines,
                 brief=self.options.brief))
        if self.options.recursive:
            result = self.deepcheck(*self.args)
        else:
            file1 = self.args[0]
            if os.path.isdir(self.args[1]):
                file2 = os.path.join(self.args[1],
                                     os.path.split(self.args[0])[-1])
            else:
                file2 = self.args[1]
            result = self.docheck(file1, file2)
        if result:
            return 1
        else:
            return 0

    def docheck(self, file1, file2):
        """Initiate comparing of two files.
"""
        lines1 = [ CmpLine(i, self.optdict)
                   for i in CFile(open(file1, 'r'), self.iscomment,
                                  self.optdict.get("ignore_space", False)) ]
        lines2 = [ CmpLine(i, self.optdict)
                   for i in CFile(open(file2, 'r'), self.iscomment,
                                  self.optdict.get("ignore_space", False)) ]
        res = ''.join(difflib.context_diff(lines1, lines2,
                                           file1, file2,
                                           n=self.optdict.get('context', 3)))
        print res,
        return bool(res)

        worker = NumDiff(cline=" ".join(sys.argv),
                         options=self.optdict)
        result = worker.compare(file1, file2)
        return result

    @staticmethod
    def deepglob(iDir):
        """Glob for whole directory subtree.
"""
        oDir = glob.glob(os.path.join(iDir, '*'))
        [ oDir.extend(glob.iglob(os.path.join(i, '*')))
          for i in oDir if os.path.isdir(i) ]
        return oDir

    @staticmethod
    def shorttree(tree, iDir):
        """Shorten list `tree` with entries from parsing a directory
tree for the base dir part `iDir`.
"""
        if iDir.endswith(os.path.sep):
            i = len(iDir)
        else:
            i = len(iDir)+1
        return [ j[i:] for j in tree ]

    @staticmethod
    def lstcomp(lst1, lst2):
        """Compare list for common enties and replace missing entries
by `None`.

    >>> Main().lstcomp([1,2,3,5,6], [1,3,4,5])
    [(1, 1), (2, None), (3, 3), (None, 4), (5, 5), (6, None)]
    >>> Main().lstcomp([1,3,4,5], [1,2,3,5,6])
    [(1, 1), (None, 2), (3, 3), (4, None), (5, 5), (None, 6)]
    >>> Main().lstcomp([1], [2,3,4,5,6])
    [(1, None), (None, 2), (None, 3), (None, 4), (None, 5), (None, 6)]
    >>> Main().lstcomp([2,3,4,5,6], [1])
    [(None, 1), (2, None), (3, None), (4, None), (5, None), (6, None)]
    >>> Main().lstcomp([2,4,6], [1,3,5])
    [(None, 1), (2, None), (None, 3), (4, None), (None, 5), (6, None)]
    >>> Main().lstcomp([1,3,5], [2,4,6])
    [(1, None), (None, 2), (3, None), (None, 4), (5, None), (None, 6)]
    >>> Main().lstcomp([1,3,5], [])
    [(1, None), (3, None), (5, None)]
    >>> Main().lstcomp([], [1,2,3])
    [(None, 1), (None, 2), (None, 3)]
"""
        ilst1 = iter(sorted(lst1))
        ilst2 = iter(sorted(lst2))
        result =  []
        for el1 in ilst1:
            try:
                el2 = ilst2.next()
            except StopIteration:
                el2 = None
            if el1 == el2 or el2 is None:
                result.append((el1, el2))
            elif el1 in lst2:
                while not el2 in lst1:
                    result.append((None, el2))
                    el2 = ilst2.next()
                result.append((el1, el2))
            elif el2 in lst1:
                while not el1 in lst2:
                    result.append((el1, None))
                    el1 = ilst1.next()
                result.append((el1, el2))
            elif el1 < el2:
                result.append((el1, None))
                result.append((None, el2))
            else:
                result.append((None, el2))
                result.append((el1, None))
        for el2 in ilst2:
            result.append((None, el2))
        return result

    def iscomment(self, line):
        """is argument line a comment line?
"""
        return (bool(self.optdict.get('cchars', '#')) and
                line.startswith(self.optdict.get('cchars', '#')))

    def dirtreecomp(self, dir1, dir2):
        """Compare two directory trees for common enties.
"""
        tree1 = self.deepglob(dir1)
        tree2 = self.deepglob(dir2)
        xtree1 = self.shorttree(tree1, dir1)
        xtree2 = self.shorttree(tree2, dir2)
        for i in xtree1:
            pass
        return self.lstcomp(xtree1, xtree2)

    @staticmethod
    def onlyIn(base, name):
        """Genereate 'Only In' message.

>>> Main.onlyIn('dir1', 'entry1')
"""
        print >> sys.stderr, "Only in %s: %s." % (base, name)


    def deepcheck(self, dir1, dir2):
        """Intiate comparison of files in two directories.
"""
        if not os.path.isdir(dir1):
            raise ValueError("'%s' is not directory" % dir1)
        if not os.path.isdir(dir2):
            raise ValueError("'%s' is not directory" % dir2)
        composite = self.dirtreecomp(dir1, dir2)
        failed = False
        for i, j in composite:
            if j is None:
                self.onlyIn(dir1, i)
                continue
            elif i is None:
                self.onlyIn(dir2, j)
                continue
            obj1 = fileFactory(i, dir1)
            obj2 = fileFactory(j, dir2)
            # print >> sys.stderr, "File %s while file %s" % (obj1, obj2)
            # print >> sys.stderr, obj1.__class__, obj2.__class__
            if ((obj1.__class__ != obj2.__class__) and
                not (isinstance(obj1, RegularFile) and
                     isinstance(obj2, RegularFile))):
                print >> sys.stderr, "File %s while file %s" % (obj1, obj2)
                failed = True
            else:
                failed = self.docheck(obj1.name(), obj2.name()) or failed
        raise NotImplementedError("ERROR ***: Not implemented yet.")

    def parse_cmdline(self):
        """
Parse command line.
"""
        option_list = [
            make_option("-c", "--comment-char",
                        action="store", type="string",
                        default=None,
                        metavar="<comment char>",
                        help="""Ignore lines starting with the comment
char when reading either file. Default: Do not ignore any line."""),
            make_option ("-e", "--reps",
                         type="float", default=1e-5, metavar="<rEPS>",
                         help="""Relative error to be accepted in
numerial comparisons. Default: %default"""),
            make_option ("-a", "--aeps",
                         type="float", default=1e-8, metavar="<aEPS>",
                         help="""Relative error to be accepted in
numerial comparisons. Default: %default"""),

            make_option ("-C", "--context",
                         type="int", default="3", metavar="<LINES>",
                         help="""Number of context lines to be
reported. Default: %default"""),
            make_option ("-b", "--ignore-space-change",
                         action="store_true",
                         help="""Ignore changes in the amount of
white space."""),
            make_option ("-s", "--splitre",
                         type="str", default=None,
                         help="""python regular expression used to split
lines before checking for numerical changes"""),
            make_option ("-r", "--recursive",
                         default=False, action="store_true",
                         help="""Recursively compare any subdirectories
found."""),

            make_option ("-I", "--ignore-matching-lines", metavar="RE",
                         type="str", default=None,
                         help="""Ignore changes whose lines all match RE."""),
            make_option ("-q", "--brief",
                         action="store_true",
                         help="""Output only whether files differ."""),
            ]

        parser = OptionParser(usage=self.DOC, option_list=option_list)

        (self.options, self.args) = parser.parse_args()

        if len(self.args) != 2:
            parser.error("incorrect number of arguments")

def _test():
    """
run doctests
"""
    import doctest

    import numdiff

    (failed, dummy) = doctest.testmod(numdiff, verbose=True)
    if failed != 0:
        raise SystemExit(10)

if __name__ == "__main__":
    MAIN = Main()
    raise SystemExit(MAIN())

# Local Variables:
# mode:python
# mode:flyspell
# compile-command:"make -C ../../test test"
# End:
