#!/bin/bash
# add to end of file /home/pi/.config/lxsession/LXDE-pi/autostart
@python3 /home/pi/Desktop/Smart_Recycle_Bin/app.py
@chromium-browser http://localhost:8080/

