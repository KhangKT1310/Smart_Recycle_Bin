#!/bin/bash

# Mở terminal mới để chạy app.py và hiển thị log
gnome-terminal --title="Run Log" -- bash -c 'python3 /home/khangkt/Desktop/Smart_Recycle_Bin/app.py; read'

# Tiếp tục thực hiện các công việc khác
sleep 1

export DISPLAY=:0  # Đảm bảo hiển thị được set đúng
google-chrome http://localhost:1234/

