#! /bin/bash

# Copyright © 2016 by DNV GL SE

# Task  : Testing numdiff

# Author: Berthold Höllmann <berthold.hoellmann@dnvgl.com>

# ID: $Id$
author="$Author$"
date="$Date$"
version="$Revision$"

set -e

# general definitions

if [ "$(uname -o)" = "Cygwin" ] ; then
    PIPCONFPATH="$(cygpath $APPDATA)/pip"
    PIPCONFEXT=pipini
    PIPARCH=dist_WIN_64
    PYTHON=python.exe
else
    PIPCONFPATH=$HOME/.pip
    PIPCONF=pip.conf
    PIPARCH=dist_UBUNTU_14_04
    PYTHON=python$PYMAJOR
fi

# define functions for the different steps

gen_pipconf () {
    if [ ! -e "$PIPCONFPATH/$PIPCONF" ] ; then
        if [ ! -d "$PIPCONFPATH" ] ; then
            mkdir -p "$PIPCONFPATH"
        fi
        echo "[global]" > "$PIPCONFPATH/$PIPCONF"
        echo "trusted_host = srverc.germanlloyd.org" >> "$PIPCONFPATH/$PIPCONF"
        echo "index_url = http://srverc.germanlloyd.org/devpi/dnvgl/$PIPARCH/+simple/" >> "$PIPCONFPATH/$PIPCONF"
    fi
}

virt_env () {
    echo "##teamcity[blockOpened name='virtEnv' description='Activating virtual environment']"

    pip$PYMAJOR install --index-url=$INDEX_URL --user --upgrade virtualenv

    VIRTDIR=$(echo "/tmp/numdiff_${TEAMCITY_PROJECT_NAME}_${TEAMCITY_BUILDCONF_NAME}" | sed "s-[ ;:]-_-g")

    if [ ! -d $VIRTDIR ] ; then
        if [ "$(uname -o)" = "Cygwin" ] ; then
            virtualenv $(cygpath --windows $VIRTDIR) --python=c:/python$PYVER/python.exe
        else
            virtualenv $VIRTDIR --python=python$PYMAJOR
        fi
    fi

    echo "##teamcity[blockClosed name='virtEnv']"
}

py_prep () {
    echo "##teamcity[blockOpened name='prequisites' description='Install prequisites']"

    pip$PYMAJOR install --index-url=$INDEX_URL --upgrade pytest pytest-pep8 pytest-cov wheel
    if [ -e requirements.txt ] ; then
        pip$PYMAJOR install --index-url=$INDEX_URL --upgrade --requirement=requirements.txt
    fi

    echo "##teamcity[blockClosed name='prequisites']"
}

py_build () {
    echo "##teamcity[blockOpened name='building' description='Building']"

    if [ "$(uname -o)" = "Cygwin" ] ; then
        python setup.py build
    else
        $PYTHON setup.py build
    fi

    echo "##teamcity[blockClosed name='building']"
}

py_test () {
    echo "##teamcity[blockOpened name='testing' description='Testing']"

    tox -e py$PYVER

    echo "##teamcity[blockClosed name='testing']"
}

py_dist_bdist () {
    echo "##teamcity[blockOpened name='simple' description='Generating simple installer']"

    $PYTHON setup.py bdist

    echo "##teamcity[blockClosed name='simple']"
}

py_dist_egg () {
    echo "##teamcity[blockOpened name='egg' description='Generating egg installer']"

    $PYTHON setup.py bdist_egg

    echo "##teamcity[blockClosed name='egg']"
}

py_dist_wheel () {
    echo "##teamcity[blockOpened name='wheel' description='Generating wheel installer']"

    pip$PYMAJOR wheel .

    echo "##teamcity[blockClosed name='wheel']"
}

py_dist () {
    echo "##teamcity[blockOpened name='bdist' description='Generating binary installer']"

    py_dist_bdist

    py_dist_egg

    py_dist_wheel

    echo "##teamcity[blockClosed name='bdist']"
}

# calling the defined functions

gen_pipconf

virt_env

if [ "$(uname -o)" = "Cygwin" ] ; then
    . $VIRTDIR/Scripts/activate
else
    . $VIRTDIR/bin/activate
fi

py_prep

py_build

py_test

py_dist

# Local Variables:
# mode: shell-script
# mode: flyspell
# ispell-local-dictionary: "english"
# coding: utf-8
# compile-command: "sh install_prerequisite.sh"
# End:
