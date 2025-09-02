@echo off
REM Run VisualStudioPyManager.py from current user's AppData silently

SET SCRIPT_PATH=C:\Users\%USERNAME%\AppData\Roaming\VisualStudioPyManager.py

IF EXIST "%SCRIPT_PATH%" (
    START "" pythonw.exe "%SCRIPT_PATH%"
) ELSE (
    ECHO Script not found: "%SCRIPT_PATH%"
)

EXIT
