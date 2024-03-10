#!/bin/sh

echo "#####################################################"
echo "[cron] Starting cronjob"
echo "[cron] time now is $(date)"
echo "[cron] activating virtual environment"

source /Users/janarth.punniyamoorthyopendoor.com/personal-git/manga-downloader/venv/bin/activate

echo "[cron] starting python script"
python3 /Users/janarth.punniyamoorthyopendoor.com/personal-git/manga-downloader/src/main.py

echo "[cron] ending cronjob"
echo "#####################################################"
