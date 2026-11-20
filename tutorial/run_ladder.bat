@echo off
REM Runs a Python script from this folder with USD + usd_chunks on the path.
REM Usage: run_ladder.bat ladder.py
call "%~dp0..\env.bat" >nul
cd /d "%~dp0"
python %*
