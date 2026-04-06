@echo off
cd /d "%~dp0"
echo Starting Tool Manager...
start /min python tool_manager.py
ping 127.0.0.1 -n 4 >nul
start "" http://localhost:5001
echo Server started. Browser opened.
timeout /t 2 >nul
exit
