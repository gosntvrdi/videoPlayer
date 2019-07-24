@echo off
taskkill /F /IM obs64.exe
timeout /T 5 /nobreak >nul
start "" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\OBS Studio\OBS Studio (64bit)"
exit
