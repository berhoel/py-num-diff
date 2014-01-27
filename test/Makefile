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

TESTS =
TESTS += esrD_test
TESTS += utf-8_test
TESTS += test_test
TESTS += dir_test
TESTS += stest_ctest
TESTS += itest_ctest
TESTS += first_atest
TESTS += NASTRAN_atest
TESTS += second_atest
TESTS += third_atest
TESTS += run4_atest
TESTS += run5_atest
TESTS += first_ctest
TESTS += second_ctest
TESTS += third_ctest
TESTS += fourth_ctest
TESTS += comma_ctest
TESTS += recur_test
TESTS += recur2_test
TESTS += mlab_test
TESTS += reps_ctest

ifeq ("$(shell uname | cut --characters 1-6)","CYGWIN")
TESTCLASS=WIN
PYPATH = PYTHONPATH=".;../lib"
else
PYPATH = PYTHONPATH=.:../lib
endif
PY_EXE = python
PYTHON = $(PYPATH) $(PY_EXE)
NUMDIFF=PATH="../app:$(PATH)" $(PYPATH) $(PY_EXE) -c "from numdiff import main;main()"

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

esrD_test:	$(PY) ref/esrD ref/d2
	$(NUMDIFF) -r ref/esrD ref/d2
	touch $@

%_test: %.py $(PY)
	$(PYTHON) $<
	touch $@

first_aopt = --comment-char='\#'
second_aopt = --reps=2e-3
third_aopt = --reps=2e-3
NASTRAN_aopt = --comment-char='$$' --fixcols=8,24,40,56,72,80
%_atest:	$(PY) ref/%1.txt ref/%2.txt
	$(PYTHON) -c "from numdiff import main;main()" $($*_aopt) ref/$*1.txt ref/$*2.txt
	touch $@

run4_atest:	$(PY) ref/third1.txt ref/third2.txt
	$(PYTHON) -c "from numdiff import main;main()" ref/third1.txt ref/third2.txt --aeps=1e-11 ; [ $$? -eq 1 ]
	touch $@

run5_atest:	$(PY) ref/mixed1.txt ref/mixed2.txt
	$(PYTHON) -c "from numdiff import main;main()" -b ref/mixed1.txt ref/mixed2.txt
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
	-$(NUMDIFF) -r ref/1 ref/2 --exclude=.svn | tee $@.txt
	diff -b $@.txt ref/$@.txt$(TESTCLASS)
	touch $@

utf-8_test:	$(PY) ref/utf-8.1.txt ref/utf-8.2.txt
	$(NUMDIFF) ref/utf-8.1.txt ref/utf-8.2.txt
	touch $@


clean:
	rm -f $(TESTS)
	[ -n "$(IGN)" ] && rm -rf $(IGN) || true

.PHONY:	build	install

dist:
	$(MAKE) -C .. $@

vpath %.py ../lib/numdiff

# Local Variables:
# compile-command:"make test"
# coding:utf-8
# End:
