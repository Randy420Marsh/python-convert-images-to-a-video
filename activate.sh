#!/bin/bash

venv_dir="venv"

python_cmd="python3.10"

$python_cmd -V
which ffmpeg
which ffplay

echo "You can now install the requirements using:"
echo ""
echo source ./$venv_dir/bin/activate
echo pip install --upgrade pip
echo pip install -r requirements.txt

# Create and activate virtual environment
if [ -d "./$venv_dir" ]; then
    source ./$venv_dir/bin/activate
else
    $python_cmd -m venv $venv_dir
    source ./$venv_dir/bin/activate
fi
