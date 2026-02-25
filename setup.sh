#!/bin/bash

echo "Установка зависимостей для Telegram бота..."

# Install Python dependencies
pip install -r requirements.txt

echo "Зависимости установлены!"
echo "Для запуска бота:"
echo "1. Создайте файл .env с вашим TELEGRAM_BOT_TOKEN"
echo "2. Выполните команду: python bot.py"