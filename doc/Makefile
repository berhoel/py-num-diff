# Copyright (C) 2012 by Germanischer Lloyd SE, 2018 DNV GL SE

# ======================================================================
# Task      Generate documentation for numdiff
# ----------------------------------------------------------------------
# Author    Berthold Hoellmann <hoel@GL-group.com>
# Project   numdiff
# ======================================================================

# ID: $Id$

SHELL = /bin/sh

DOC_HOST=wwwsoftware@intranet
DOC_DIR=/export/www/intranet/html/intranet/pool/ho/software/info/numdiff

PYNAME = python
export PYTHONPATH := ../build/lib

all test:

doc:
	[ -d numdiff_doc ] || mkdir numdiff_doc
	PYTHONPATH=$(PYTHONPATH) python -c "from epydoc.cli import cli ; cli()"	\
  --config numdiff.ini -v --inheritance included
	chmod -R a+r numdiff_doc

install: doc
	scp -r numdiff_doc/* $(DOC_HOST):$(DOC_DIR)


# Local Variables:
# mode:makefile
# compile-command:"make"
# coding:utf-8
# End:
