#!/bin/bash
# script that will watch th process list for process with name 'python -m nomad', stop it at 10:00 PM and start it at 5:00 AM
# also restart the process if the logfile was not updated in the last 20 minutes
# This script will be run by cron job every 10 minutes
# Cron job to run the script every 10 minutes
# */10 * * * * /path/to/scheduler.sh
# Author: David Kovacs

# variables
LOG_PATH=/home/nomadserver/nomad/log/nomad.log
START_HOUR=5
STOP_HOUR=22

# get the process id of the process with name 'python -m nomad'
pid=$(ps -ef | grep 'python -m nomad' | grep -v grep | awk '{print $2}')

# get the current time in epoch
current_time=$(date +%s)

# get the current hour
current_hour=$(date +%H)

# get the last modified time of the logfile
last_modified=$(stat -c %Y $LOG_PATH)

# get the difference between the current time and the last modified time of the logfile
time_diff=$((current_time - last_modified))

# if the process is running and time_diff is greater than 1200 seconds (20 minutes), restart the process
if [ -n "$pid" ] && [ "$time_diff" -gt 1200 ]; then
    kill -9 $pid
    python -m nomad &
fi


# if the process is running and the current hour is STOP_HOUR, stop the process
if [ -n "$pid" ] && [ "$current_hour" -eq "$STOP_HOUR" ]; then
    kill -9 $pid
fi


# if the process is not running and the current hour is START_HOUR, start the process
if [ -z "$pid" ] && [ "$current_hour" -eq "$START_HOUR" ]; then
    python -m nomad &
fi

# end of script
