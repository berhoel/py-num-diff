#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Testing routines in the numdiff module.
"""

import os.path
# Standard libraries.
import re

# Third party libraries.
import pytest
# DNV GL libraries.
from numdiff import Main

__date__ = "2022/04/30 19:10:30 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2014 by Germanischer Lloyd SE, 2019 by DNV GL SE"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berthold.hoellmann@dnvgl.com"


class TestMain(object):
    def test_columns_001(self):
        assert Main.columns("8,24,40,56,72,80") == [8, 24, 40, 56, 72, 80]

    def test_columns_002(self):
        assert Main().columns("8,24,40,56,72,80") == [8, 24, 40, 56, 72, 80]

    def test_lstcomp_001(self):
        assert Main.lstcomp([1, 2, 3, 5, 6], [1, 3, 4, 5]) == [
            (1, 1),
            (2, None),
            (3, 3),
            (None, 4),
            (5, 5),
            (6, None),
        ]

    def test_lstcomp_002(self):
        assert Main().lstcomp([1, 2, 3, 5, 6], [1, 3, 4, 5]) == [
            (1, 1),
            (2, None),
            (3, 3),
            (None, 4),
            (5, 5),
            (6, None),
        ]

    def test_lstcomp_003(self):
        assert Main.lstcomp([1, 3, 4, 5], [1, 2, 3, 5, 6]) == [
            (1, 1),
            (None, 2),
            (3, 3),
            (4, None),
            (5, 5),
            (None, 6),
        ]

    def test_lstcomp_004(self):
        assert Main().lstcomp([1, 3, 4, 5], [1, 2, 3, 5, 6]) == [
            (1, 1),
            (None, 2),
            (3, 3),
            (4, None),
            (5, 5),
            (None, 6),
        ]

    def test_lstcomp_005(self):
        assert Main.lstcomp([1], [2, 3, 4, 5, 6]) == [
            (1, None),
            (None, 2),
            (None, 3),
            (None, 4),
            (None, 5),
            (None, 6),
        ]

    def test_lstcomp_006(self):
        assert Main().lstcomp([1], [2, 3, 4, 5, 6]) == [
            (1, None),
            (None, 2),
            (None, 3),
            (None, 4),
            (None, 5),
            (None, 6),
        ]

    def test_lstcomp_007(self):
        assert Main().lstcomp([2, 3, 4, 5, 6], [1]) == [
            (None, 1),
            (2, None),
            (3, None),
            (4, None),
            (5, None),
            (6, None),
        ]

    def test_lstcomp_008(self):
        assert Main().lstcomp([2, 4, 6], [1, 3, 5]) == [
            (None, 1),
            (2, None),
            (None, 3),
            (4, None),
            (None, 5),
            (6, None),
        ]

    def test_lstcomp_009(self):
        assert Main().lstcomp([1, 3, 5], [2, 4, 6]) == [
            (1, None),
            (None, 2),
            (3, None),
            (None, 4),
            (5, None),
            (None, 6),
        ]

    def test_lstcomp_010(self):
        assert Main.lstcomp([1, 3, 5], []) == [(1, None), (3, None), (5, None)]

    def test_lstcomp_011(self):
        assert Main.lstcomp([], [1, 2, 3]) == [(None, 1), (None, 2), (None, 3)]

    @pytest.fixture(scope="class")
    def main_1(self):
        return Main()

    def test_shorttree_1_001(self, main_1):
        assert main_1.shorttree(
            iDir="ref/1", *("ref/1", ["1", ".svn"], ["2", "3", "4"])
        ) == ["1", ".svn", "2", "3", "4"]

    def test_shorttree_1_002(self, main_1):
        assert [
            "/".join(os.path.split(i))
            for i in main_1.shorttree(iDir="ref/1", *("ref/1/1", [".svn"], []))
        ] == ["1/.svn"]

    def test_shorttree_1_003(self, main_1):
        assert list(
            [
                "/".join(os.path.split(i))
                for i in main_1.shorttree(
                    iDir="ref/1",
                    *(
                        "ref/1/1/.svn",
                        ["text-base", "prop-base", "props", "tmp"],
                        ["entries", "all-wcprops"],
                    )
                )
            ]
        ) == [
            "1/.svn/text-base",
            "1/.svn/prop-base",
            "1/.svn/props",
            "1/.svn/tmp",
            "1/.svn/entries",
            "1/.svn/all-wcprops",
        ]

    def test_shorttree_1_004(self, main_1):
        assert main_1.shorttree(iDir="esrD", *("esrD", [], ["data.txt"])) == [
            "data.txt"
        ]

    @pytest.fixture(scope="class")
    def main_2(self):
        res = Main()
        res.exclude = re.compile(r"\.svn").match
        return res

    def test_shorttree_2_001(self, main_2):
        assert main_2.shorttree(
            iDir="ref/1", *("ref/1", ["1", ".svn"], ["2", "3", "4"])
        ) == ["1", "2", "3", "4"]

    def test_shorttree_2_002(self, main_2):
        assert main_2.shorttree(iDir="ref/1", *("ref/1/1", [".svn"], [])) == []

    def test_shorttree_2_003(self, main_2):
        assert (
            main_2.shorttree(
                iDir="ref/1",
                *(
                    "ref/1/1/.svn",
                    ["text-base", "prop-base", "props", "tmp"],
                    ["entries", "all-wcprops"],
                )
            )
            == []
        )


True


# Local Variables:
# mode: python
# compile-command: "python ../../../setup.py test"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
