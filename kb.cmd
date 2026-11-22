@echo off
rem Wrapper: runs tools\kb.py with the project virtualenv.
setlocal
set "KB_PY=%~dp0.venv\Scripts\python.exe"
if not exist "%KB_PY%" set "KB_PY=python"
"%KB_PY%" "%~dp0tools\kb.py" %*
exit /b %ERRORLEVEL%
