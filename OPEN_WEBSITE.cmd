@echo off
setlocal

cd /d "%~dp0"

where py >nul 2>nul
if errorlevel 1 (
  echo Python launcher ^(py^) was not found.
  echo Please install Python 3 from https://www.python.org/downloads/
  pause
  exit /b 1
)

start "Local Web Server" cmd /k py -3 -m http.server 5500
timeout /t 1 >nul
start "" http://127.0.0.1:5500/index.html

endlocal
