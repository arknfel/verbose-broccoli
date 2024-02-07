#!/usr/bin/env bash

set -euo pipefail

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPTPATH/../businesslogic/$1

# Create venv
rm -rf packagevenv
python3 -m venv packagevenv

# Create package
mkdir -p package
rm -rf package/*
rm -f package.md5sum
rm -f package.zip

# Install dependencies
packagevenv/bin/pip install -r requirements.txt

# Move source-code to package
RUNTIME=$( ls -l packagevenv/lib | grep python | awk '{print $NF}' )
cp -R packagevenv/lib/$RUNTIME/site-packages/* package
cp src/*.* package

cd package

find . -exec touch -t "197001010000" '{}' +
zip -rq -D -X ../package.zip . -x"*.pyc" -x "*__pycache__*"

cd ..

# Cleanup venv
rm -rf packagevenv

# Cleanup libs
rm -rf libs.zip libs

# Delpoy source-code to lambda
aws lambda update-function-code --function-name $1 --zip-file fileb://package.zip

rm -rf package*
