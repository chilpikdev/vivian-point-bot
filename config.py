"""
Configuration settings for the Telegram Points Bot
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the bot"""
    
    # Telegram Bot Token
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # API credentials (loaded from environment variables)
    API_BASE_URL = os.getenv('API_BASE_URL')
    API_USERNAME = os.getenv('API_USERNAME')
    API_PASSWORD = os.getenv('API_PASSWORD')
    
    # Check if required environment variables are set
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
    
    if not API_BASE_URL or not API_USERNAME or not API_PASSWORD:
        raise ValueError("API configuration (API_BASE_URL, API_USERNAME, API_PASSWORD) is required")
    
    # Default welcome message
    WELCOME_MESSAGE = (
        "Привет! 👋\n\n"
        "Для проверки ваших баллов, пожалуйста, отправьте свой контакт нажав на кнопку ниже. 👇"
    )
    
    # Message when user is not a client
    NOT_CLIENT_MESSAGE = "❌ Вы не являетесь клиентом"
    
    # Message template for showing points
    POINTS_MESSAGE_TEMPLATE = "✅ Вы являетесь клиентом!\n💰 Ваши баллы: {}"
    
    # Error message for invalid contact
    INVALID_CONTACT_MESSAGE = "❌ Вы можете отправить только свой собственный контакт."
    
    # Contact button text
    CONTACT_BUTTON_TEXT = "📱 Отправить контакт"
    
    # Check again button text
    CHECK_AGAIN_BUTTON_TEXT = "🔄 Проверить еще раз"