@echo off
REM Cooks the saved ladder network three more times with different drivers.
call "%~dp0..\env.bat" >nul
cd /d "%~dp0"
python -m usd_chunks.cli run ladder_network.usda Rails.sy=2 -o ladder_short.usda
python -m usd_chunks.cli run ladder_network.usda Rails.sy=5 Rung.sx=0.8 Rung.ty=0.5 -o ladder_tall_wide.usda
python -m usd_chunks.cli run ladder_network.usda Rung.ty=0.15 -o ladder_dense.usda
