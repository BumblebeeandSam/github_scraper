#!/bin/bash
# Bashscript to run ChinaScraper.py


echo "Running ChinaScraper!" >> "log"
now=$(date +"%T")
echo "Current time: $now" >> "log"
today=$(date +"%m/%d/%y")
echo "Current Date: $today" >> "log"

python3 ChinaScraper.py

echo "Completed running ChinaScraper.py!" >> "log"
now=$(date +"%T")
echo "Current time: $now" >> "log"
today=$(date +"%m/%d/%y")
echo "Current Date: $today" >> "log"
