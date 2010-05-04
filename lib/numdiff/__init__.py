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
import fnmatch
import os
import os.path
import re
import sys
from itertools import izip, chain, repeat
from optparse import OptionParser, make_option

import numpy as np

from .files import fileFactory, RegularFile, Directory
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
        self.exclude = lambda x:None
        self.ignore_matching_lines = lambda x:None
        self.differ = None

    def __call__(self):
        self.parse_cmdline()
        self.optdict.update(
            dict(cchars=self.options.comment_char,
                 aeps=self.options.aeps,
                 reps=self.options.reps,
                 ignore_space=self.options.ignore_space_change,
                 splitre=self.options.splitre,
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
        if bool(res):
           if self.options.brief:
               print "Files %s and %s differ" % (file1, file2)
           else:
               print res,
        return bool(res)

    def shorttree(self, base, dirs, fnames, iDir):
        """Shorten list `tree` with entries from parsing a directory
tree for the base dir part `iDir`.

>>> w = Main()
>>> print w.shorttree(iDir='ref/1', *('ref/1', ['1', '.svn'], ['2', '3', '4']))
['1', '.svn', '2', '3', '4']
>>> print w.shorttree(iDir='ref/1', *('ref/1/1', ['.svn'], []))
['1/.svn']
>>> print w.shorttree(iDir='ref/1', *('ref/1/1/.svn', ['text-base', 'prop-base', 'props', 'tmp'],
...                                   ['entries', 'all-wcprops']))
['1/.svn/text-base', '1/.svn/prop-base', '1/.svn/props', '1/.svn/tmp', '1/.svn/entries', '1/.svn/all-wcprops']
>>> w.exclude = re.compile(r'\.svn').match
>>> print w.shorttree(iDir='ref/1', *('ref/1', ['1', '.svn'], ['2', '3', '4']))
['1', '2', '3', '4']
>>> print w.shorttree(iDir='ref/1', *('ref/1/1', ['.svn'], []))
[]
>>> print w.shorttree(iDir='ref/1', *('ref/1/1/.svn', ['text-base', 'prop-base', 'props', 'tmp'],
...                                   ['entries', 'all-wcprops']))
[]
"""
        if self.exclude(os.path.split(base)[-1]):
            return []

        if iDir.endswith(os.path.sep):
            i = len(iDir)
        else:
            i = len(iDir)+1
        lBase = base[i:]
        return [ os.path.join(lBase, i)
                 for i in dirs+fnames
                 if not self.exclude(i) ]

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
        return ((bool(self.optdict.get('cchars', '#')) and
                 line.startswith(self.optdict.get('cchars', '#'))) or
                self.ignore_matching_lines(line))

    def dirtreecomp(self, dir1, dir2):
        """Compare two directory trees for common enties.
"""
        tree1 = os.walk(dir1)
        tree2 = os.walk(dir2)
        res_tree1 = []
        res_tree2 = []
        for xtree1, xtree2 in izip(tree1, tree2):
            dirs, files = xtree1[1:]
            for i in dirs[::-1]:
                if self.exclude(i):
                    dirs.remove(i)
            for i in files[::-1]:
                if self.exclude(i):
                    files.remove(i)
            res_tree1 += self.shorttree(iDir=dir1, *xtree1)
            dirs, files = xtree2[1:]
            for i in dirs[::-1]:
                if self.exclude(i):
                    dirs.remove(i)
            for i in files[::-1]:
                if self.exclude(i):
                    files.remove(i)
            res_tree2 += self.shorttree(iDir=dir2, *xtree2)
        return self.lstcomp(res_tree1, res_tree2)

    @staticmethod
    def onlyIn(base, name):
        """Genereate 'Only In' message.

>>> Main.onlyIn('dir1', 'entry1')
Only in dir1: entry1.
"""
        print "Only in %s: %s." % (base, name)


    def deepcheck(self, dir1, dir2):
        """Intiate comparison of files in two directories.
"""
        if not os.path.isdir(dir1):
            raise ValueError("'%s' is not directory" % dir1)
        if not os.path.isdir(dir2):
            raise ValueError("'%s' is not directory" % dir2)
        failed = False
        composite = self.dirtreecomp(dir1, dir2)
        for i, j in composite:
            if j is None:
                self.onlyIn(dir1, i)
                failed = True
                continue
            elif i is None:
                self.onlyIn(dir2, j)
                failed = True
                continue
            obj1 = fileFactory(i, dir1)
            obj2 = fileFactory(j, dir2)
            if ((obj1.__class__ != obj2.__class__) and
                not (isinstance(obj1, RegularFile) and
                     isinstance(obj2, RegularFile))):
                print "File %s while file %s" % (obj1, obj2)
                failed = True
            elif not isinstance(obj1, Directory):
                failed = self.docheck(obj1.name, obj2.name) or failed
        return failed

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
                         type="float", default=1e-5, metavar="rEPS",
                         help="""Relative error to be accepted in
numerial comparisons. Default: %default"""),
            make_option ("-a", "--aeps",
                         type="float", default=1e-8, metavar="aEPS",
                         help="""Relative error to be accepted in
numerial comparisons. Default: %default"""),
            make_option ("-C", "--context",
                         type="int", default="3", metavar="LINES",
                         help="""\
Output NUM (default %default) lines of copied context."""),
#             make_option ("-U", "--unified",
#                          type="int", default="3", metavar="LINES",
#                          help="""\
# Output NUM (default %default) lines of unified context."""),
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
            make_option ("-x", "--exclude", metavar='PAT', default=[],
                         action='append', help="""\
Exclude files that match PAT."""),
            make_option ("-I", "--ignore-matching-lines", metavar="RE",
                         type="str", default=[], action='append',
                         help="""Ignore changes whose lines all match RE."""),
            make_option ("-q", "--brief",
                         action="store_true",
                         help="""Output only whether files differ."""),
            ]

        parser = OptionParser(usage=self.DOC, option_list=option_list)

        (self.options, self.args) = parser.parse_args()

        if len(self.args) != 2:
            parser.error("incorrect number of arguments")

        if self.options.exclude:
            self.exclude = re.compile('|'.join([fnmatch.translate(i) for i in self.options.exclude])).match

        if self.options.ignore_matching_lines:
            self.ignore_matching_lines = re.compile('|'.join(self.options.ignore_matching_lines)).search

def _test():
    """
run doctests
"""
    import doctest

    module = __import__(__name__)

    (failed, dummy) = doctest.testmod(module, verbose=True)
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
