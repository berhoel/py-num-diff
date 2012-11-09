# Copyright (C) 2006 by Germanischer Lloyd AG

# ======================================================================
# Task      Make tasks for numdiff
# ----------------------------------------------------------------------
# Author    Berthold Hoellmann <hoel@GL-group.com>
# Project   numdiff
# ======================================================================


# ID: $Id$

SHELL = /bin/sh

IGN = $(shell [ -n "$$(svn propget svn:ignore .)" ] && \
	echo "$$(svn propget svn:ignore .)")

all:	build

test:
	$(MAKE) -C test $@

build:
	python setup.py build

install:	test
	python setup.py install

clean:
	[ -n "$(IGN)" ] && $(RM) -r $(IGN) || true
	$(MAKE) -C test clean

dist:	build
	python setup.py bdist_egg

.PHONY:	build	test	dist

# Local Variables:
# compile-command:"make test"
# coding:utf-8
# End:
