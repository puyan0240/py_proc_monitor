@echo off
if exist ".\venv" (
    echo already setup !!
) else (
    echo setup starting ...
    python -m venv venv

    call .\venv\Scripts\activate.bat
    python -m pip install -U pip
    python -m pip install -r requirement.txt
    call deactivate.bat

    echo ------------------------------------------
    echo setup complete !!
    echo ------------------------------------------
)