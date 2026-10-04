@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

:: Change to script directory
cd /d "%~dp0"

where uv >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    uv run python -X utf8 tarot.py
    goto end
)

if exist "%USERPROFILE%\.local\bin\uv.exe" (
    "%USERPROFILE%\.local\bin\uv.exe" run python -X utf8 tarot.py
    goto end
)

where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    py -3 -X utf8 tarot.py
    goto end
)

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    python -X utf8 tarot.py
    goto end
)

echo [ERROR] Python or uv was not found on your system.
pause

:end
