# Copyright (C) 2006 by Germanischer Lloyd AG

# ======================================================================
# Task      testing tasks for numdiff
# ----------------------------------------------------------------------
# Author    Berthold Hoellmann <hoel@GL-group.com>
# Project   numdiff
# ======================================================================

# ID: $Id$

SHELL = /bin/sh

PY = $(shell ls ../lib/numdiff/*.py)

TESTS = numdiff_doctest cmpline_doctest files_doctest		\
	test_test dir_test split_test ignore_test		\
	run1_test run2_test run3_test run4_test run5_test	\
	call1_test call2_test call3_test call4_test		\
	comma_test recur_test recur2_test mlab_test

PYPATH = PYTHONPATH=../lib
PYTHON = $(PYPATH) python
NUMDIFF=PATH=../app:$(PATH) $(PYPATH) numdiff

IGN = $(shell [ -n "$$(svn propget svn:ignore .)" ] && echo "$$(svn propget svn:ignore .)")

all:	build

test: $(TESTS)

build:
	$(MAKE) -C .. $@

install:	test
	$(MAKE) -C .. $@

%_test: %.py $(PY)
	$(PYTHON) $<
	touch $@

run1_test:	$(PY) ref/first1.txt ref/first2.txt
	$(PYTHON) ../app/numdiff ref/first1.txt ref/first2.txt --comment-char='#'
	touch $@

run2_test:	$(PY) ref/second1.txt ref/second2.txt
	$(PYTHON) ../app/numdiff ref/second1.txt ref/second2.txt --reps=2e-3
	touch $@

run3_test:	$(PY) ref/third1.txt ref/third2.txt
	$(PYTHON) ../app/numdiff ref/third1.txt ref/third2.txt --reps=2e-3
	touch $@

run4_test:	$(PY) ref/third1.txt ref/third2.txt
	$(PYTHON) ../app/numdiff ref/third1.txt ref/third2.txt --aeps=1e-11 ; [ $$? -eq 1 ]
	touch $@

run5_test:	$(PY) ref/mixed1.txt ref/mixed2.txt
	$(PYTHON) ../app/numdiff -b ref/mixed1.txt ref/mixed2.txt
	touch $@

call1_test:	$(PY) ref/first1.txt ref/first2.txt
	$(NUMDIFF) ref/first1.txt ref/first2.txt --comment-char='#'
	touch $@

call2_test:	$(PY) ref/second1.txt ref/second2.txt
	$(NUMDIFF) ref/second1.txt ref/second2.txt --reps=2e-3
	touch $@

call3_test:	$(PY) ref/third1.txt ref/third2.txt
	$(NUMDIFF) ref/third1.txt ref/third2.txt --reps=2e-5
	touch $@

call4_test:	$(PY) ref/third1.txt ref/third2.txt
	$(NUMDIFF) ref/third1.txt ref/third2.txt --aeps=1e-11 ; [ $$? -eq 1 ]
	touch $@

comma_test:	$(PY) ref/comma1.txt ref/comma2.txt
	$(NUMDIFF) ref/comma1.txt ref/comma2.txt
	touch $@

dir_test:	$(PY) ref/d1/data.txt ref/d2/data.txt
	$(NUMDIFF) ref/d1/data.txt ref/d2
	touch $@

recur_test:	$(PY) ref/d1/data.txt ref/d2/data.txt
	$(NUMDIFF) -r ref/d1 ref/d2 --exclude=.svn
	touch $@

recur2_test:	$(PY) ref/d1/data.txt ref/d2/data.txt
	-$(NUMDIFF) -r ref/1 ref/2 --exclude=.svn > $@.txt
	diff $@.txt ref
	touch $@

split_test:	$(PY) ref/stest1.txt ref/stest2.txt
	$(NUMDIFF) -s "\\|" ref/stest1.txt ref/stest2.txt
	touch $@

ignore_test:	$(PY) ref/stest1.txt ref/stest2.txt
	$(NUMDIFF) -I REV -s "\\|" ref/itest1.txt ref/itest2.txt
	touch $@

numdiff_doctest:	$(PY)
	$(PYTHON) -c "import numdiff ; numdiff._test()" -v 
	touch $@

mlab_test:
	$(NUMDIFF) --matlab ref/mlab_R2007b ref/mlab_R2012a
	touch $@

%_doctest:	%.py	$(PY)
	$(PYTHON) -c "from numdiff import $* ; $*._test()" -v 
	touch $@

clean:
	rm -f $(TESTS)
	[ -n "$(IGN)" ] && rm -f $(IGN) || true

.PHONY:	build	install

vpath %.py ../lib/numdiff

# Local Variables:
# compile-command:"make test"
# coding:utf-8
# End:
