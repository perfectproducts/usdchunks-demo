@echo off
REM Runs every example script in usd_chunks\examples; results go to .\output
setlocal
call "%~dp0env.bat"
set EX=%USDCHUNKS_HOME%\usd_chunks\examples
if not exist "%USDCHUNKS_HOME%\output" mkdir "%USDCHUNKS_HOME%\output"
pushd "%USDCHUNKS_HOME%\output"
for %%S in (box shot_setup cubes_mesh_or_gprim biome ivy_wall shot_departments use_groups) do (
    echo ==== %%S
    python "%EX%\scripts\%%S.py" || echo !!!! %%S FAILED
)
echo ==== build_groups (to output\groups)
if not exist groups mkdir groups
python "%EX%\groups\build_groups.py" groups || echo !!!! build_groups FAILED
popd
endlocal
