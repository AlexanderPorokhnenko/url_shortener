#!/usr/bin/env bash

PYTHONCMD=python3.8

MAINDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${MAINDIR}"
MAINDIR=$PWD

$PYTHONCMD -m venv env
source env/bin/activate
$PYTHONCMD -m pip install --upgrade pip setuptools
$PYTHONCMD -m pip install -r requirements.txt
