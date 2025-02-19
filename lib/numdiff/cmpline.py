#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class for allowing numerical diffing of text lines.
"""

# Standard libraries.
import re

__date__ = "2022/04/30 19:08:23 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2010 by Germanischer Lloyd SE, 2019 by DNV GL SE"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berthold.hoellmann@dnvgl.com"


__all__ = ["CmpLine"]

_FLOAT = re.compile(r"\s*[-+]?(\d+(\.\d*)?|\d*\.\d+)([eE][-+]?\d+)?\s*")
_INT = re.compile(r"\s*[-+]?\d+(?![.eE])\s*")


class CmpLine(object):
    """Representing test lines to be compared.

    Tries literal comparison of lines first. If this fails, tries
    numerical comparison.

    >>> a, b, c = CmpLine("AA 1.00000000001"), CmpLine("AA 1"), CmpLine("BB")
    >>> a == c
    False
    >>> a == b
    True"""

    linesplit = re.compile(r" *, *| +")

    def __init__(self, line, options=None):
        self.line = line
        if options is None:
            self.options = {"fixcols": None}
        else:
            self.options = options
        self.value = self.line
        if self.options.get("ignore_space_change"):
            self.value = self.value.strip()
        self.ignore = None
        if self.options.get("ignore") is not None:
            self.ignore = re.compile(self.options["ignore"])
        if self.options.get("splitre"):
            self.linesplit = re.compile(self.options["splitre"])
        self.aeps = self.options.get("aeps", 1e-8)
        self.reps = self.options.get("reps", 1e-5)

    def __eq__(self, other):
        if self.options.get("verbose"):
            print("__EQ__ !%s! !%s!" % (self.value.strip(), other.value.strip()))
        if (
            self.ignore is not None
            and self.ignore.search(self.value)
            and self.ignore.search(other.value)
        ):
            if self.options.get("verbose"):
                print("IGNORE !%s! !%s!" % (self.value.strip(), other.value.strip()))
            return True
        elif self.value.strip() == other.value.strip():
            if self.options.get("verbose"):
                print("EQUAL !%s! !%s!" % (self.value.strip(), other.value.strip()))
            return True
        else:
            sLine1 = self.splitline(self.value.strip())
            sLine2 = self.splitline(other.value.strip())
            if len(sLine1) != len(sLine2):
                if self.options.get("verbose"):
                    print(
                        "SPLITLEN !%s! !%s!" % (self.value.strip(), other.value.strip())
                    )
                return False
            for token1, token2 in zip(sLine1, sLine2):
                if self.options.get("verbose"):
                    print("token1: ", token1, "; token2: ", token2)
                if self.options.get("ignore_space", False):
                    token1 = token1.strip()
                    token2 = token2.strip()
                if token1 == token2:
                    continue
                elif _FLOAT.match(token1) or _FLOAT.match(token2):
                    if self.options.get("verbose"):
                        print(
                            "FLOAT !%s! !%s!"
                            % (self.value.strip(), other.value.strip())
                        )
                    try:
                        if self.fequals(float(token1), float(token2)):
                            continue
                    except ValueError:
                        if self.options.get("verbose"):
                            print(
                                "ValueError !%s! !%s!"
                                % (self.value.strip(), other.value.strip())
                            )
                elif _INT.match(token1) or _INT.match(token2):
                    if self.options.get("verbose"):
                        print(
                            "INT !%s! !%s!" % (self.value.strip(), other.value.strip())
                        )
                    if self.fequals(int(token1), int(token2)):
                        continue

                if self.options.get("verbose"):
                    print("TOKEN !%s! !%s!" % (self.value.strip(), other.value.strip()))
                return False
            if self.options.get("verbose"):
                print("SAME !%s! !%s!" % (self.value.strip(), other.value.strip()))
            return True

    def fequals(self, float1, float2):
        """Check for arguments beeing numerical equal."""
        if self.options.get("verbose"):
            print(
                "fequals: ",
                float1,
                float2,
                abs(float1 - float2),
                (self.aeps + self.reps * abs(float2)),
            )

        return abs(float1 - float2) <= (self.aeps + self.reps * abs(float2))

    def splitline(self, line):
        """Split line into tokens to be evaluated."""
        if self.options["fixcols"]:
            return [
                line[i:j]
                for i, j in zip(
                    [0] + self.options["fixcols"][:-1], self.options["fixcols"]
                )
            ]
        else:
            return self.linesplit.split(line)

    def __str__(self):
        return self.line

    def __radd__(self, other):
        return other + self.value

    def __len__(self):
        return len(self.value)

    def __getitem__(self, item):
        return self.value[item]

    def __hash__(self):
        return 1


# Local Variables:
# mode: python
# compile-command: "python ../../setup.py test"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
