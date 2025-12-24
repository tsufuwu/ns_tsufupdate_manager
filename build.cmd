@echo off
chcp 65001 > nul
title PyInstaller Build Script

REM Chuyển thư mục làm việc về nơi chứa file .cmd
cd /d "%~dp0"

echo ==============================
echo Building executable...
echo Current directory:
echo %cd%
echo ==============================

python -m PyInstaller ^
 --name="SWITCH.TSUFUPDATER.MANAGER" ^
 --noconsole ^
 --onefile ^
 --icon="icon.ico" ^
 --add-data "logo.png;." ^
 --add-data "loading.gif;." ^
 --add-data "icon.ico;." ^
 "Nsupdate.py"

echo ==============================
echo Build finished.
echo Output is in the /dist folder.
echo ==============================

pause
