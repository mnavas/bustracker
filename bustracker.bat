@echo off
REM BusTracker CLI — Windows entry point
REM Usage: bustracker <command>
cd /d "%~dp0"
python bustracker.py %*
