#!/usr/bin/env bash

# if account unliked run linkAccount.sh
# then run main.py

# $1 is the nake of the new linked device

./linkAccount.sh $1

python3 main.py