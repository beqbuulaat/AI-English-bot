#!/usr/bin/env python3
"""
Main entry point for the Telegram English Learning Bot.
Handles webhook setup and Flask server initialization.
"""

import os
import logging
from flask import Flask, request
from bot import TelegramBot

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize bot
bot = TelegramBot()

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming webhook from Telegram."""
    try:
        update = request.get_json()
        if update:
            bot.handle_update(update)
        return 'OK', 200
    except Exception as e:
        logger.error(f"Error handling webhook: {e}")
        return 'Error', 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return 'Bot is running!', 200

@app.route('/setup_webhook', methods=['GET'])
def setup_webhook():
    """Setup webhook for the bot."""
    # Get the current URL from the request and ensure it's HTTPS for Replit
    base_url = request.url_root.rstrip('/')
    if base_url.startswith('http://'):
        base_url = base_url.replace('http://', 'https://')
    
    webhook_url = base_url + '/webhook'
    
    try:
        # First, let's check current webhook info
        check_url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/getWebhookInfo"
        import requests
        check_response = requests.get(check_url)
        current_webhook = check_response.json()
        
        # Set new webhook
        result = bot.set_webhook(webhook_url)
        
        return f'''
        <!DOCTYPE html>
        <html>
        <head><title>Webhook Setup</title><meta charset="UTF-8"></head>
        <body>
            <h1>🔧 Информация о Webhook</h1>
            <p><strong>Устанавливаемый URL:</strong> {webhook_url}</p>
            <p><strong>Результат установки:</strong> {'✅ Успешно' if result else '❌ Ошибка'}</p>
            
            <h2>Текущее состояние webhook:</h2>
            <pre>{current_webhook}</pre>
            
            <h2>Тестирование бота:</h2>
            <p>Теперь попробуйте отправить <code>/start</code> боту @GrammerBuddyBot в Telegram</p>
            
            <p><a href="/">← Вернуться на главную</a></p>
        </body>
        </html>
        '''
    except Exception as e:
        return f'''
        <h1>❌ Ошибка: {str(e)}</h1>
        <p>Возможные причины:</p>
        <ul>
            <li>Неверный токен бота</li>
            <li>Проблемы с сетью</li>
            <li>URL должен быть HTTPS</li>
        </ul>
        <p><a href="/">← Вернуться на главную</a></p>
        '''

@app.route('/', methods=['GET'])
def index():
    """Basic index page."""
    webhook_setup_url = request.url_root.rstrip('/') + '/setup_webhook'
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>English Learning Bot</title>
        <meta charset="UTF-8">
    </head>
    <body>
        <h1>🤖 English Learning Telegram Bot</h1>
        <p>Bot is running and ready to help you learn English!</p>
        
        <h2>🔧 Настройка:</h2>
        <p><a href="{webhook_setup_url}" style="background: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Настроить Webhook</a></p>
        
        <h2>Features:</h2>
        <ul>
            <li>Word and phrase translation (EN ↔ RU)</li>
            <li>Interactive quizzes for levels A1-B2</li>
            <li>Progress tracking</li>
            <li>Vocabulary practice</li>
            <li><strong>🤖 AI-powered tutoring</strong></li>
            <li>Grammar explanations</li>
            <li>Text analysis and correction</li>
            <li>Personalized learning advice</li>
        </ul>
        <h2>Basic Commands:</h2>
        <ul>
            <li>/start - Start using the bot</li>
            <li>/help - Get help information</li>
            <li>/translate - Translate words or phrases</li>
            <li>/quiz - Start a vocabulary quiz</li>
            <li>/level - Set your English level</li>
            <li>/progress - Check your progress</li>
        </ul>
        <h2>🤖 AI Commands:</h2>
        <ul>
            <li>/ai - AI tutor help</li>
            <li>/explain - Explain grammar topics</li>
            <li>/analyze - Analyze English text</li>
            <li>/correct - Check text for errors</li>
            <li>/advice - Get personalized learning advice</li>
        </ul>
    </body>
    </html>
    '''

if __name__ == '__main__':
    # Get configuration from environment
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'
    
    # Set webhook if WEBHOOK_URL is provided
    webhook_url = os.getenv('WEBHOOK_URL')
    if webhook_url:
        bot.set_webhook(f"{webhook_url}/webhook")
        logger.info(f"Webhook set to: {webhook_url}/webhook")
    
    # Start Flask server
    logger.info(f"Starting bot server on {host}:{port}")
    app.run(host=host, port=port, debug=False)
