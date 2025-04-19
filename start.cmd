@echo off
echo ========================================================================================================================
echo Hello, Thanks For Installing Aina-chan Discord Bot
echo ========================================================================================================================
echo This script will install cloudflared to run in your windows, if it doesn't exist I mean...
echo Then it'll automatically run the server and the discord bot...
echo Oh, you're using linux???
echo I'll... Figure it out later...
echo Let's start then...
echo Sorry, I'm just tired...
@echo off

REM Check if virtual environment exists, create if it doesn't
if not exist venv\ (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\scripts\activate

REM Install dependencies
echo Installing required packages...
pip install -r requirements.txt

REM Download cloudflared if needed
if not exist cloudflared.exe (
    echo Downloading cloudflared...
    curl -Lo cloudflared.exe https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe
)

REM Start the server
echo Starting Cloudflare Tunnel
start cmd /k "cloudflared.exe tunnel --url localhost:5453"

echo Starting FastAPI Server
start cmd /k "uvicorn app.main:app --reload --port 5453"