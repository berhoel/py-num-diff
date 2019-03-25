# Copyright (C) 2006 by Germanischer Lloyd AG, 2019 DNV GL SE

# ======================================================================
# Task      Make tasks for numdiff
# ----------------------------------------------------------------------
# Author    Berthold Hoellmann <hoel@GL-group.com>
# Project   numdiff
# ======================================================================


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
	$(MAKE) -C doc install

doc:	build
	$(MAKE) -C doc doc

clean:
	[ -n "$(IGN)" ] && $(RM) -r $(IGN) || true
	for i in $$(find . -type d | grep -v .svn) ; do			\
 [ -n "$$(svn propget svn:ignore $$i)" ] &&				\
  (cd $$i ; $(RM) -rr "$$(svn propget svn:ignore .)") || true ;	\
done
	$(MAKE) -C test clean

dist:	build
	python setup.py bdist_egg

.PHONY:	build	test	dist	doc

# Local Variables:
# compile-command:"make test"
# coding:utf-8
# End:
