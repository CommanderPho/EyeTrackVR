:: Example script to auto build app and make an installer
:: File paths will all need to be updated to your setup
@REM cd C:\Users\pho\repos\ExternalTesting\EyeTrackVR\EyeTrackApp
cd C:\Users\Pho\repos\EyeTrackVR\EyeTrackApp

poetry run python eyetrackapp.py
@REM cd C:\Users\pho\repos\ExternalTesting\EyeTrackVR\
@REM poetry run python EyeTrackApp\eyetrackapp.py
@echo off
color 0A
echo -------------------------------
echo ############ DONE #############
echo -------------------------------
PAUSE