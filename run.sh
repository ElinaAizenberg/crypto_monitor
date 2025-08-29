#!/bin/bash

# Telegram Crypto Price Monitor Bot Runner

echo "🤖 Starting Telegram Crypto Price Monitor Bot..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Run 'python setup.py' to configure the bot first."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Run the bot
echo "🚀 Starting bot..."
python main.py