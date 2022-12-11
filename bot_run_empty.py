#!/bin/bash

# Should we redirect bash output?
# Use the following
# command > .../path_to_file/
#set echo off

# Bot token as enviroment variable
export TOKEN='YourBot:Token'
#echo $TOKEN
# start bot (we can redirect output from this script)
python bot_telegram.py
