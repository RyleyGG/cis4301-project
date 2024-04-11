#!/bin/bash

if [ ! -f ./backend/.env ]; then
    echo "Creating .env file with default values..."

    oracle_username=$(dd if=/dev/urandom bs=32 count=1 2>/dev/null | base64)
    oracle_password=$(dd if=/dev/urandom bs=32 count=1 2>/dev/null | base64)

    echo "oracle_username=$oracle_username" >> .env
    echo "oracle_password=$oracle_password" >> .env
fi

if [ ! -d ./backend/.venv ]; then
    echo "Creating and initializing python virtual environment..."
    python -m venv ./backend/.venv
    echo "Activating the virtual environment..."
    source ./backend/.venv/Scripts/activate
    pip install -r backend/requirements.txt
fi

if [ -f "./backend/api_start.sh" ]; then
    chmod u+rwx "./backend/api_start.sh"
    dos2unix "./backend/api_start.sh"
else
    echo "Could not find api_start.sh file. Your repository may be corrupted, or need to be re-pulled."
fi

if [ -f "./nuke.sh" ]; then
    chmod u+rwx "./nuke.sh"
    dos2unix "./nuke.sh"
else
    echo "Could not find nuke.sh file. Your repository may be corrupted, or need to be re-pulled."
fi

if [ -f "./run.sh" ]; then
    chmod u+rwx "./run.sh"
    dos2unix "./run.sh"
else
    echo "Could not find run.sh file. Your repository may be corrupted, or need to be re-pulled."
fi


if [ -f "./mini_nuke.sh" ]; then
    chmod u+rwx "./mini_nuke.sh"
    dos2unix "./mini_nuke.sh"
else
    echo "Could not find mini_nuke.sh file. Your repository may be corrupted, or need to be re-pulled."
fi

cd frontend
npm install