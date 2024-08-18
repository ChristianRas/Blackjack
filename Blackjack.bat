@ECHO off

set "script_path=%~dp0"
set "script_path=%script_path%Blackjack.py"
python %script_path% %*
pause