#!/usr/bin/env bash

set -euo pipefail

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd ${SCRIPTPATH}/$1

VENV=venv

# Create venv
rm -rf ${VENV}
python3 -m venv ${VENV}

# Create package
mkdir -p package
rm -rf package/*
rm -f package.md5sum
rm -f package.zip

# Install dependencies
${VENV}/bin/pip install -r requirements.txt

# Move source-code to package
RUNTIME=$( ls -l ${VENV}/lib | grep python | awk '{print $NF}' )
cp -R ${VENV}/lib/${RUNTIME}/site-packages/* package
cp src/*.* package

cd package

find . -exec touch -t "197001010000" '{}' +
zip -rq -D -X ../package.zip . -x"*.pyc" -x "*__pycache__*"

cd ..

# Cleanup venv
rm -rf ${VENV}

# Cleanup libs
rm -rf libs.zip libs
