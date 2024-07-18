#!/usr/bin/env bash

# $1 = name of device

$(signal-cli link -n $1 > linkOutput.txt &)
sleep 10
qrencode -t ANSI -r linkOutput.txt
echo "script will exit in 30 seconds don't ctrl-c" 
sleep 30
rm linkOutput.txt

