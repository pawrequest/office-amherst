@echo off
set dotNetVersion=0
reg query "HKLM\SOFTWARE\Microsoft\Active Setup\Installed Components\{3C3901C5-3455-3E0A-A214-0B093A5070A6}"
@echo %ERRORLEVEL%
if %ERRORLEVEL% EQU 0 set dotNetVersion=1 

reg query "HKLM\SOFTWARE\Microsoft\Active Setup\Installed Components\{F5B09CFD-F0B2-36AF-8DF4-1DF6B63FC7B4}"
@echo %ERRORLEVEL%
if %ERRORLEVEL% EQU 0 set dotNetVersion=1 

if %dotNetVersion% EQU 1 goto end

:VC2010CHX86Install
echo Installing Microsoft .Net Framwork 4.0
dotNetFx40_Full_x86_x64.exe /q

:end
exit