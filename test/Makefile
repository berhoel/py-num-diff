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
	test_test dir_test stest_ctest itest_ctest		\
	first_atest second_atest third_atest run4_atest run5_atest	\
	first_ctest second_ctest third_ctest fourth_ctest		\
	comma_ctest recur_test recur2_test mlab_test reps_ctest

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

mlab_test:	$(PY) ref/mlab_R2007b ref/mlab_R2012a
	$(NUMDIFF) --matlab ref/mlab_R2007b ref/mlab_R2012a
	touch $@

%_test: %.py $(PY)
	$(PYTHON) $<
	touch $@

first_aopt = --comment-char='\#'
second_aopt = --reps=2e-3
third_aopt = --reps=2e-3
%_atest:	$(PY) ref/%1.txt ref/%2.txt
	$(PYTHON) ../app/numdiff $($*_aopt) ref/$*1.txt ref/$*2.txt
	touch $@

run4_atest:	$(PY) ref/third1.txt ref/third2.txt
	$(PYTHON) ../app/numdiff ref/third1.txt ref/third2.txt --aeps=1e-11 ; [ $$? -eq 1 ]
	touch $@

run5_atest:	$(PY) ref/mixed1.txt ref/mixed2.txt
	$(PYTHON) ../app/numdiff -b ref/mixed1.txt ref/mixed2.txt
	touch $@

first_copt = --comment-char='\#'
second_copt = --reps=2e-3
third_copt = --reps=2e-5
stest_copt = -s "\\|"
itest_copt =  -I REV -s "\\|"
%_ctest:	$(PY) ref/%1.txt ref/%2.txt
	$(NUMDIFF) $($*_copt) ref/$*1.txt ref/$*2.txt
	touch $@

reps_ctest:	$(PY) ref/reps1.txt ref/reps2.txt
	-$(NUMDIFF) -e .09 --context=0 ref/reps1.txt ref/reps2.txt | tee $@.txt
	diff $@.txt ref
	touch $@

fourth_ctest:	$(PY) ref/third1.txt ref/third2.txt
	$(NUMDIFF) ref/third1.txt ref/third2.txt --aeps=1e-11 ; [ $$? -eq 1 ]
	touch $@

dir_test:	$(PY) ref/d1/data.txt ref/d2/data.txt
	$(NUMDIFF) --verbose ref/d1/data.txt ref/d2
	touch $@

recur_test:	$(PY) ref/d1/data.txt ref/d2/data.txt
	$(NUMDIFF) -r ref/d1 ref/d2 --exclude=.svn
	touch $@

recur2_test:	$(PY) ref/d1/data.txt ref/d2/data.txt
	-$(NUMDIFF) -r ref/1 ref/2 --exclude=.svn > $@.txt
	diff -b $@.txt ref
	touch $@

numdiff_doctest:	$(PY)
	$(PYTHON) -c "import numdiff ; numdiff._test()" -v
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
