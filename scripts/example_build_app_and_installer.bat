:: Example script to auto build app and make an installer
:: File paths will all need to be updated to your setup
cd C:\Users\pho\repos\ExternalTesting\EyeTrackVR\EyeTrackApp
pyinstaller eyetrackapp.spec --noconfirm
cd C:\Users\pho\Desktop
cd C:\Program Files (x86)\Inno Setup 6
ISCC C:\Users\pho\Desktop\Output\ETVR_SETUP.iss
cls
@echo off
color 0A
echo -------------------------------
echo ############ DONE #############
echo -------------------------------
PAUSE