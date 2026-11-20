@echo off
REM One-time setup: clones usd_chunks (pinned) and installs its Python deps into .\deps
REM using the Python that ships with the NVIDIA OpenUSD build in C:\usd_root.
setlocal
set ROOT=%~dp0
if not exist "%ROOT%usd_chunks" (
    git clone https://github.com/HuginStudios/usd_chunks.git "%ROOT%usd_chunks" || exit /b 1
    git -C "%ROOT%usd_chunks" checkout dba1f3a9526b3728735cc3e5f567018b8c05057b
)
C:\usd_root\python\python.exe -m pip install --target "%ROOT%deps" attrs typing-extensions numpy scipy requests mujoco fast-simplification
endlocal
