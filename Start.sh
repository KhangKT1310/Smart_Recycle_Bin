#!/bin/bash
# add to end of file /home/pi/.config/lxsession/LXDE-pi/autostart
@python3 /home/pi/Desktop/Smart_Recycle_Bin/app.py
@python3 -m http.server 8000 --directory /home/pi/Desktop/Smart_Recycle_Bin/
@chromium-browser http://localhost:8000/templates/index.html

