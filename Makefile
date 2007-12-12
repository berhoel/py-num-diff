# Copyright (C) 2006 by Germanischer Lloyd AG

# ======================================================================
# Module    Makefile
# Task      Testing for numdiff
# ----------------------------------------------------------------------
# Author    Berthold Höllmann <hoel@GL-Group.com>
# Project   GLPy
# ----------------------------------------------------------------------
# Status    $State: Exp $
# Date      $Date: 2007-12-12 14:34:09 $
# ======================================================================

# CVSID: $Id: Makefile,v 1.5 2007-12-12 14:34:09 hoel Exp $

SHELL = /bin/sh

PY = numdiff.py

TESTS = test_test run1_test run2_test run3_test run4_test	\
	call1_test call2_test call3_test call4_test		\
	comma_test

all:	build

test: $(TESTS)

build:
	python setup.py build

install:	test
	python setup.py install

%_test: %.py $(PY)
	python $<
	touch $@

run1_test:	$(PY) ref/first1.txt  ref/first2.txt
	python numdiff.py ref/first1.txt  ref/first2.txt --comment-char='#'
	touch $@

run2_test:	$(PY) ref/second1.txt  ref/second2.txt
	python numdiff.py ref/second1.txt  ref/second2.txt --reps=2e-3
	touch $@

run3_test:	$(PY) ref/third1.txt  ref/third2.txt
	python numdiff.py ref/third1.txt  ref/third2.txt --reps=2e-3
	touch $@

run4_test:	$(PY) ref/third1.txt  ref/third2.txt
	python numdiff.py ref/third1.txt  ref/third2.txt --aeps=1e-11 ; [ $$? -eq 1 ]
	touch $@

call1_test:	$(PY) ref/first1.txt  ref/first2.txt
	./numdiff ref/first1.txt  ref/first2.txt --comment-char='#'
	touch $@

call2_test:	$(PY) ref/second1.txt  ref/second2.txt
	./numdiff ref/second1.txt  ref/second2.txt --reps=2e-3
	touch $@

call3_test:	$(PY) ref/third1.txt  ref/third2.txt
	./numdiff ref/third1.txt  ref/third2.txt --reps=2e-5
	touch $@

call4_test:	$(PY) ref/third1.txt  ref/third2.txt
	./numdiff ref/third1.txt  ref/third2.txt --aeps=1e-11 ; [ $$? -eq 1 ]
	touch $@

comma_test:	$(PY) ref/comma1.txt  ref/comma2.txt
	./numdiff ref/comma1.txt  ref/comma2.txt
	touch $@

clean:
	rm -f $(TESTS)

.PHONY:	build	install

# Local Variables:
# compile-command:"make test"
# End:
