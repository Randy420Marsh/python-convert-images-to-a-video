@echo off

setlocal enabledelayedexpansion

set "venv_dir=venv"

echo Virtual environment activated. You are now using Python from !venv_dir!.
python -V
where ffmpeg
where ffplay
echo.
echo You can now install the requirements using:
echo pip install -r .\requirements.txt
echo.

if not exist !venv_dir! (
    python -m venv !venv_dir!
)

cmd /k call !venv_dir!\Scripts\activate.bat