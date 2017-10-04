#!/usr/bin/env bash

PYTHONPATH=$(pwd)
for f in tests/test_*.py
do
 py.test -vv -s $f
done
