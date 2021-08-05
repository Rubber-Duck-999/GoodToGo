#!/bin/sh

echo 'Starting'
python3 /home/pi/Documents/GoodToGo/main.py &

python3 /home/pi/Documents/HouseGuardServices/Notifier/main.py
