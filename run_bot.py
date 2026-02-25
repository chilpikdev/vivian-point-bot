#!/usr/bin/env python3
"""
Script to run the Telegram Points Bot
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages from requirements.txt"""
    print("Installing required packages...")
    result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    if result.returncode != 0:
        print("Failed to install requirements")
        sys.exit(1)
    print("Requirements installed successfully")

def run_bot():
    """Run the Telegram bot"""
    print("Starting the Telegram Points Bot...")
    os.system("python bot.py")

if __name__ == "__main__":
    install_requirements()
    run_bot()