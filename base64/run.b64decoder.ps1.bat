@echo off
echo.
powershell -ExecutionPolicy Bypass -File b64decoder.ps1 -InputFile example.txt
timeout /t 10