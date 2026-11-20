@echo off
REM Opens usdview with the usd_chunks plugin. Usage: usdview_chunks.bat [file.usda]
REM With no file, opens the box example network.
setlocal
call "%~dp0env.bat"
set FILE=%~1
if "%FILE%"=="" set FILE=%USDCHUNKS_HOME%\output\box_network.usda
call C:\usd_root\bin\usdview.cmd "%FILE%"
endlocal
