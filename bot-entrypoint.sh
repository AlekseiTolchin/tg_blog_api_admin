#!/bin/bash
set -e
echo "Starting Telegram bot..."
cd /app
PYTHONPATH=/app exec python bot/run.py
