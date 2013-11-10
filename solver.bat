@echo off

rem Display help info if appropiate parameters are passed
if "%1"=="-?" (
goto RunSolver
)
if "%1%"=="--help" (
goto RunSolver
)

set /P graphFileName="Enter graph filename: "
set /P numTravellers="How many travellers?: "
:RunSolver
call python solver.py --guiFormat --filename=%graphFileName% --travellers=%numTravellers% %*

if not %ERRORLEVEL%==0 (
pause
goto End
)

call python solverGUI.py --filename=%graphFileName%

:End
