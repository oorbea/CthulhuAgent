#!/bin/bash

if [ ! -d ".venv" ]; then
    python3 -m venv .venv || python -m venv .venv
fi

source .venv/bin/activate

pip install -r requirements.txt
clear
python3 app.py || python app.py
