@echo off
cd /d "C:\Users\Diego\Desktop\DulcesPercy"
start "" "http://127.0.0.1:8000"
py manage.py runserver
pause
