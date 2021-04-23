@if (@CodeSection == @Batch) @then


@echo off
setlocal EnableDelayedExpansion

rem Multi-line menu with options selection via DOSKEY
rem Define the options
set numOpts=0
for %%a in (Scan Run) do (
   set /A numOpts+=1
   set "option[!numOpts!]=%%a"
)
set /A numOpts+=1
set "option[!numOpts!]=Exit"

rem Clear previous doskey history
doskey /REINSTALL
rem Fill doskey history with menu options
cscript //nologo /E:JScript "%~F0" EnterOpts
for /L %%i in (1,1,%numOpts%) do set /P "var="

:nextOpt
cls
echo NeosVR HRM System
echo ==================
echo Version 2.0 By RaithSphere
echo.
rem Send a F7 key to open the selection menu
cscript //nologo /E:JScript "%~F0"
set /P "var=Select option: "
echo/
if "%var%" equ "Exit" goto :EOF
if "%var%" equ "Scan" goto :scan
if "%var%" equ "Run" goto :run
echo Option selected: "%var%"
pause
goto nextOpt

:scan
cls
echo Bluetooth Scan
python HRM.py -s
echo.
echo Edit the file config.conf with the MAC Address for the device required!
echo.
pause
goto nextOpt

:run
cls
echo Starting BT Client, press CTRL+C TWICE to end or close this window
echo.
python HRM.py
pause


@end

var wshShell = WScript.CreateObject("WScript.Shell"),
    envVar = wshShell.Environment("Process"),
    numOpts = parseInt(envVar("numOpts"));

if ( WScript.Arguments.Length ) {
   // Enter menu options
   for ( var i=1; i <= numOpts; i++ ) {
      wshShell.SendKeys(envVar("option["+i+"]")+"{ENTER}");
   }
} else {
   // Enter a F7 to open the menu
   wshShell.SendKeys("{F7}{HOME}");
}