#!/bin/sh

echo "#####################################################"
echo "Starting cronjob"
echo "time now is $(date)"

source /Users/janarth.punniyamoorthyopendoor.com/personal-git/manga-downloader/venv/bin/activate

echo "starting python script"
python3 /Users/janarth.punniyamoorthyopendoor.com/personal-git/manga-downloader/src/main.py

echo "ending cronjob"
echo "#####################################################"
