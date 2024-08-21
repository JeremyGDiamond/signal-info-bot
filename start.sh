#!/usr/bin/env bash

# if account unliked run linkAccount.sh
# then run main.py

# $1 is the nake of the new linked device

ERROR=$(signal-cli receive 2>&1 >/dev/null)

if [ "$ERROR" = "No local users found, you first need to register or link an account" ]; then
    ./linkAccount.sh $1
else
    echo "already linked"
fi

python3 main.py