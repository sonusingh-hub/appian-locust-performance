#!/bin/bash

CURRENT_DIR=$(dirname "$0")

pip install -U twine setuptools

python ${CURRENT_DIR}/../setup.py sdist bdist_wheel

twine check dist/*

twine upload dist/* -u $TWINE_USERNAME -p $TWINE_PASSWORD
