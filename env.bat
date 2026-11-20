@echo off
REM usd_chunks environment on top of NVIDIA's prebuilt OpenUSD in C:\usd_root.
REM Our entries are set first so set_usd_env.bat puts USD's own pip-packages (PySide6, PyOpenGL 3.1.5) ahead of them.
set USDCHUNKS_HOME=%~dp0
set USDCHUNKS_HOME=%USDCHUNKS_HOME:~0,-1%
set PYTHONPATH=%USDCHUNKS_HOME%\usd_chunks;%USDCHUNKS_HOME%\deps
set PXR_PLUGINPATH_NAME=%USDCHUNKS_HOME%\usd_chunks\usd_chunks\hosts\usdview
set USD_CHUNK_DIRS=%USDCHUNKS_HOME%\usd_chunks\chunks
call C:\usd_root\scripts\set_usd_env.bat
