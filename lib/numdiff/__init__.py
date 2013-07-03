#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
numerical diff for text files
"""

from __future__ import (print_function, division, absolute_import,
                        unicode_literals)

# ID: $Id$"
__date__ = "$Date$"[6:-1]
__version__ = "$Revision$"[10:-1]
__author__ = "`Berthold Höllmann <berthold.hoellmann@GL-group.com>`__"
__copyright__ = "Copyright © 2005 by Germanischer Lloyd SE"

import difflib
import fnmatch
import os
import os.path
import sys
import re
from argparse import ArgumentParser
if sys.version_info < (3, 1):
    from itertools import izip as zip

from .files import fileFactory, RegularFile, Directory
from .cmpline import CmpLine
from .difflist import DiffList

#  CVSID: $Id$
__date__ = u"$Date$"[5:-1]
__version__ = "$Revision$"[10:-1]
__docformat__ = "restructuredtext en"

__all__ = ['Main']


class NumDiffError(SystemExit):
    """Standard Error indicator for NumDiff
"""
    pass


# See http://www.unix.org/single_unix_specification/
def context_diff(sequence, a, b, fromfile='', tofile='',
                 fromfiledate='', tofiledate='', n=3, lineterm='\n'):
    r"""
Modified context_diff taken from stamdard Python difflib.

This version takes
"""
    from difflib import _format_range_context, SequenceMatcher

    prefix = dict(insert='+ ', delete='- ', replace='! ', equal='  ')
    started = False
    seq = SequenceMatcher(None, [], [])
    seq.opcodes = sequence
    for group in seq.get_grouped_opcodes(n):
        if not started:
            started = True
            fromdate = '\t{}'.format(fromfiledate) if fromfiledate else ''
            todate = '\t{}'.format(tofiledate) if tofiledate else ''
            yield '*** {}{}{}'.format(fromfile, fromdate, lineterm)
            yield '--- {}{}{}'.format(tofile, todate, lineterm)

        first, last = group[0], group[-1]
        yield '***************' + lineterm

        file1_range = _format_range_context(first[1], last[2])
        yield '*** {} ****{}'.format(file1_range, lineterm)

        if any(tag in ('replace', 'delete') for tag, _, _, _, _ in group):
            for tag, i1, i2, _, _ in group:
                if tag != 'insert':
                    for line in a[i1:i2]:
                        yield prefix[tag] + line

        file2_range = _format_range_context(first[3], last[4])
        yield '--- {} ----{}'.format(file2_range, lineterm)

        if any(tag in ('replace', 'insert') for tag, _, _, _, _ in group):
            for tag, _, _, j1, j2 in group:
                if tag != 'delete':
                    for line in b[j1:j2]:
                        yield prefix[tag] + line


class CFile(object):
    """Class for providing file information with ability to ignore
comment lines.
"""
    ws = re.compile(r"\s+")

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
                yield " ".join(CFile.ws.split(i.strip())) + '\n'
            else:
                yield i


class Main():
    """Main program. Used when called on command line.
"""
    DOC = """\
Compare two text files with taking into account numerical errors.
"""

    def __init__(self):
        self.options = None
        self.args = None
        self.optdict = {}
        self.exclude = lambda x: None
        self.ignore_matching_lines = lambda x: None
        self.differ = None

    def __call__(self):
        self.parse_cmdline()
        self.optdict.update(
            dict(cchars=self.args.comment_char,
                 aeps=self.args.aeps,
                 reps=self.args.reps,
                 ignore_space=self.args.ignore_space_change,
                 splitre=self.args.splitre,
                 brief=self.args.brief,
                 mlab=self.args.matlab,
                 verbose=self.args.verbose,
                 fixcols=self.args.fixcols))
        if self.args.matlab:
            self.optdict['ignore_space'] = True
        if self.args.recursive:
            result = self.deepcheck(self.args.from_file, self.args.to_file)
        else:
            file1 = self.args.from_file
            if os.path.isdir(self.args.to_file):
                file2 = os.path.join(self.args.to_file,
                                     os.path.split(self.args.from_file)[-1])
            else:
                file2 = self.args.to_file
            print("comparing '%s' and '%s'" % (file1, file2))
            result = self.docheck(file1, file2)
        if result:
            return 1
        else:
            return 0

    def docheck(self, file1, file2):
        """Initiate comparing of two files.
"""
        lines1 = [i.split('\n')[0]
                  for i in CFile(open(file1, 'r'), self.iscomment,
                                 self.args.ignore_space_change or
                                 self.args.matlab)]
        lines2 = [i.split('\n')[0]
                  for i in CFile(open(file2, 'r'), self.iscomment,
                                 self.args.ignore_space_change or
                                 self.args.matlab)]

        if self.optdict['mlab']:
            lines1[:6] = [''] * 6
            lines2[:6] = [''] * 6

        my_answer = DiffList(maxchunk=10)
        if self.args.verbose:
            print("difflib.SequenceMatcher(None, lines1, lines2).get_opcodes()")
            print(difflib.SequenceMatcher(None, lines1, lines2).get_opcodes())
        for (tag, ai, aj, bi, bj) in difflib.SequenceMatcher(
                None, lines1, lines2).get_opcodes():
            if tag in ('delete', 'insert', 'equal'):
                my_answer.append((tag, ai, aj, bi, bj))
            else:
                for (_, AI, AJ, BI, BJ) in DiffList.prepres(
                        tag, ai, aj, bi, bj, 20):
                    a = [CmpLine(i, self.optdict) for i in lines1[AI:AJ]]
                    b = [CmpLine(i, self.optdict) for i in lines2[BI:BJ]]
                    my_answer.extend(
                        [(i[0], i[1] + AI, i[2] + AI, i[3] + BI, i[4] + BI)
                         for i in difflib.SequenceMatcher(
                                 None, a, b).get_opcodes()])

        if self.args.verbose:
            print("lines1:")
            print(['%s' % i for i in lines1])
            print("lines2:")
            print(['%s' % i for i in lines2])
            print("my_answer")
            print(my_answer)
        res = '\n'.join(
            context_diff(
                my_answer,
                lines1, lines2, fromfile=file1, tofile=file2,
                n=self.args.context, lineterm=''))
        if bool(res):
            if self.args.brief:
                print("Files %s and %s differ" % (file1, file2))
            else:
                print(res)
        return bool(res)

    def shorttree(self, base, dirs, fnames, iDir):
        r"""Shorten list `tree` with entries from parsing a directory
tree for the base dir part `iDir`.

>>> w = Main()
>>> w.shorttree(iDir='ref/1', *('ref/1', ['1', '.svn'], ['2', '3', '4'])
...     ) == ['1', '.svn', '2', '3', '4']
True
>>> ['/'.join(os.path.split(i)) for i in w.shorttree(iDir='ref/1',
...        *('ref/1/1', ['.svn'], []))] == ['1/.svn']
True
>>> list(['/'.join(os.path.split(i)) for i in w.shorttree(iDir='ref/1',
...                   *('ref/1/1/.svn',
...                     ['text-base', 'prop-base', 'props', 'tmp'],
...                     ['entries', 'all-wcprops']))]) == [
...     '1/.svn/text-base', '1/.svn/prop-base', '1/.svn/props', '1/.svn/tmp',
...     '1/.svn/entries', '1/.svn/all-wcprops']
True
>>> w.exclude = re.compile(r'\.svn').match
>>> w.shorttree(iDir='ref/1', *('ref/1', ['1', '.svn'],
...      ['2', '3', '4'])) == ['1', '2', '3', '4']
True
>>> w.shorttree(iDir='ref/1', *('ref/1/1', ['.svn'], [])) == []
True
>>> w.shorttree(iDir='ref/1',
...             *('ref/1/1/.svn',
...               ['text-base', 'prop-base', 'props', 'tmp'],
...               ['entries', 'all-wcprops'])) == []
True
"""
        if self.exclude(os.path.split(base)[-1]):
            return []

        if iDir.endswith(os.path.sep):
            i = len(iDir)
        else:
            i = len(iDir) + 1
        lBase = base[i:]
        return [os.path.join(lBase, j)
                for j in dirs + fnames
                if not self.exclude(j)]

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
        result = []
        for el1 in ilst1:
            try:
                if sys.version_info < (3, 1):
                    el2 = ilst2.next()
                else:
                    el2 = next(ilst2)
            except StopIteration:
                el2 = None
            if el1 == el2 or el2 is None:
                result.append((el1, el2))
            elif el1 in lst2:
                while not el2 in lst1:
                    result.append((None, el2))
                    if sys.version_info < (3, 1):
                        el2 = ilst2.next()
                    else:
                        el2 = next(ilst2)
                result.append((el1, el2))
            elif el2 in lst1:
                while not el1 in lst2:
                    result.append((el1, None))
                    if sys.version_info < (3, 1):
                        el1 = ilst1.next()
                    else:
                        el1 = next(ilst1)
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
        tree1 = os.walk(dir1, topdown=True)
        tree2 = os.walk(dir2, topdown=True)
        res_tree1 = []
        res_tree2 = []
        for xtree1, xtree2 in zip(tree1, tree2):
            dirs, files = xtree1[1:]
            [dirs.remove(i) for i in dirs[::-1] if self.exclude(i)]
            [files.remove(i) for i in files[::-1] if self.exclude(i)]
            res_tree1 += self.shorttree(xtree1[0], dirs, files, iDir=dir1)
            dirs, files = xtree2[1:]
            [dirs.remove(i) for i in dirs[::-1] if self.exclude(i)]
            [files.remove(i) for i in files[::-1] if self.exclude(i)]
            res_tree2 += self.shorttree(xtree1[0], dirs, files, iDir=dir2)
        return self.lstcomp(res_tree1, res_tree2)

    @staticmethod
    def onlyIn(base, name):
        """Genereate 'Only In' message.

>>> Main.onlyIn('dir1', 'entry1')
Only in dir1: entry1.
"""
        print("Only in %s: %s." % (base, name))

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
            if i is not None:
                print("comparing '%s' and '%s'" % (
                    os.path.join(dir1, i),
                    os.path.join(dir2, j if j else i)))
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
                print("File %s while file %s" % (obj1, obj2))
                failed = True
            elif not isinstance(obj1, Directory):
                failed = self.docheck(obj1.name, obj2.name) or failed
        return failed

    @staticmethod
    def columns(inp):
        """
>>> Main.columns('8,24,40,56,72,80')
[8, 24, 40, 56, 72, 80]
"""
        return [int(i) for i in inp.split(',')]

    def parse_cmdline(self):
        """
Parse command line.
"""
        parser = ArgumentParser(description=self.DOC)
        parser.add_argument('from_file', metavar='<from file>',
                            type=str)
        parser.add_argument('to_file', metavar='<to file>', type=str)
        parser.add_argument("-c", "--comment-char", action="store",
                            metavar="<comment char>", type=str,
                            default=None, help="""Ignore lines
                            starting with the comment char when
                            reading either file. Default: Do not
                            ignore any line.""")
        parser.add_argument("-e", "--reps", type=float, default=1e-5,
                            metavar="rEPS", help="""Relative error to
                            be accepted in numerial
                            comparisons. Default: %(default)g""")
        parser.add_argument("-a", "--aeps", type=float, default=1e-8,
                            metavar="aEPS", help="""Absolute error to
                            be accepted in numerial
                            comparisons. Default: %(default)g""")
        parser.add_argument("-C", "--context", type=int, default=3,
                            metavar="LINES", help="""Output NUM
                            (default %(default)d) lines of copied
                            context.""")
        # parser.add_argument("-U", "--unified", type=int, default=3,
        #                     metavar="LINES", help="""Output NUM
        #                     (default %(default)d) lines of unified
        #                     context.""")
        parser.add_argument("-b", "--ignore-space-change",
                            action="store_true", help="""Ignore
                            changes in the amount of white space.""")
        group = parser.add_argument_group('colspec')
        group.add_argument("-s", "--splitre", type=str, default=None,
                           help="""python regular expression used to
                           split lines before checking for numerical
                           changes""")
        group.add_argument('--fixcols', type=self.columns,
                           help="""Comma separated list of columns for
                           fixed column format files""")
        parser.add_argument("-r", "--recursive", default=False,
                            action="store_true", help="""Recursively
                            compare any subdirectories found.""")
        parser.add_argument("-x", "--exclude", metavar='PAT',
                            default=[], action='append',
                            help="""Exclude files that match PAT.""")
        parser.add_argument("-I", "--ignore-matching-lines",
                            metavar="RE", type=str, default=[],
                            action='append', help="""Ignore changes
                            whose lines all match RE.""")
        parser.add_argument("-q", "--brief", action="store_true",
                            help="""Output only whether files
                            differ.""")
        parser.add_argument("--matlab", action="store_true",
                            help="""Compare MATLAB output, ignore the
                            first lines.""")
        parser.add_argument("--verbose", action="store_true",
                            help="""Generate verbose output.""")

        self.args = parser.parse_args()

        if self.args.verbose:
            print("options: aTol: %g; rTol: %g" % (
                self.args.aeps, self.args.reps))

        # if len(self.args) != 2:
        #     parser.error("incorrect number of arguments")

        if self.args.exclude:
            self.exclude = re.compile('|'.join(
                [fnmatch.translate(i) for i in self.args.exclude])).match

        if self.args.ignore_matching_lines:
            self.ignore_matching_lines = re.compile('|'.join(
                self.args.ignore_matching_lines)).search

# Local Variables:
# mode: python
# mode: flyspell
# ispell-local-dictionary: "en"
# compile-command: "make -C ../../test test"
# End:
