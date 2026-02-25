import os
import requests
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from config import Config

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command"""
    keyboard = [
        [KeyboardButton(Config.CONTACT_BUTTON_TEXT, request_contact=True)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        Config.WELCOME_MESSAGE,
        reply_markup=reply_markup
    )

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle contact messages"""
    contact = update.message.contact
    
    # Check if the contact belongs to the user who sent it
    if contact.user_id != update.effective_user.id:
        await update.message.reply_text(Config.INVALID_CONTACT_MESSAGE)
        return
    
    phone_number = contact.phone_number
    
    # Ensure phone number starts with '+' for consistent format
    if not phone_number.startswith('+'):
        phone_number = '+' + phone_number
    
    # Store phone number in user_data for "Check Again" functionality
    context.user_data['phone_number'] = phone_number
    
    # Remove the '+' sign for API request
    phone_for_api = phone_number.lstrip('+')
    
    # Make API request to check if user exists and get points
    api_url = f"{Config.API_BASE_URL}/point?phone={phone_for_api}"
    
    try:
        response = requests.get(
            api_url,
            auth=(Config.API_USERNAME, Config.API_PASSWORD),
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            # Assuming the API returns a field with the points value
            # Adjust this based on the actual API response structure
            points = data.get('point', 0) if isinstance(data, dict) else 0
            
            if points is not None:
                # Create keyboard with "Check Again" button
                keyboard = [
                    [KeyboardButton(Config.CHECK_AGAIN_BUTTON_TEXT)]
                ]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
                
                await update.message.reply_text(
                    Config.POINTS_MESSAGE_TEMPLATE.format(points),
                    reply_markup=reply_markup
                )
            else:
                await update.message.reply_text(Config.NOT_CLIENT_MESSAGE)
        else:
            # If API returns non-200 status, treat as not a client
            await update.message.reply_text(Config.NOT_CLIENT_MESSAGE)
            
    except requests.exceptions.RequestException:
        # If there's an error connecting to the API, inform the user
        await update.message.reply_text("⚠️ Ошибка при проверке данных. Попробуйте позже.")


async def handle_check_again(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle 'Check Again' button press"""
    phone_number = context.user_data.get('phone_number')
    
    if not phone_number:
        # If no phone number stored, ask to send contact again
        await start(update, context)
        return
    
    # Remove the '+' sign for API request
    phone_for_api = phone_number.lstrip('+')
    
    # Make API request to check points
    api_url = f"{Config.API_BASE_URL}/point?phone={phone_for_api}"
    
    try:
        response = requests.get(
            api_url,
            auth=(Config.API_USERNAME, Config.API_PASSWORD),
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            points = data.get('point', 0) if isinstance(data, dict) else 0
            
            if points is not None:
                # Create keyboard with "Check Again" button
                keyboard = [
                    [KeyboardButton(Config.CHECK_AGAIN_BUTTON_TEXT)]
                ]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
                
                await update.message.reply_text(
                    Config.POINTS_MESSAGE_TEMPLATE.format(points),
                    reply_markup=reply_markup
                )
            else:
                await update.message.reply_text(Config.NOT_CLIENT_MESSAGE)
        else:
            await update.message.reply_text(Config.NOT_CLIENT_MESSAGE)
            
    except requests.exceptions.RequestException:
        await update.message.reply_text("⚠️ Ошибка при проверке данных. Попробуйте позже.")

def main():
    """Main function to run the bot"""
    # Get the bot token from config
    token = Config.TELEGRAM_BOT_TOKEN
    
    # Create the Application object
    application = Application.builder().token(token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    application.add_handler(MessageHandler(filters.Text([Config.CHECK_AGAIN_BUTTON_TEXT]), handle_check_again))
    
    # Run the bot
    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()