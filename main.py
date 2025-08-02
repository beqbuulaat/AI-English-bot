import os
import telebot
import requests
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # обязательно добавим на Render

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "👋 Welcome to AI English Bot!\nSend /word <english word> to get explanation, translation and example!"
    )

@bot.message_handler(commands=['word'])
def explain_word(message):
    try:
        word = message.text.split(' ', 1)[1]
    except IndexError:
        bot.reply_to(message, "Please provide a word. Example: /word apple")
        return

    prompt = f"Explain the word '{word}' in English, translate it into Russian, and give an example sentence."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    json_data = {
        "model": "mistral:mythomax-l2",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=json_data)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        bot.send_message(message.chat.id, reply)
    else:
        bot.send_message(message.chat.id, "⚠️ Failed to get response from AI.")

# Устанавливаем webhook один раз при старте
@app.before_first_request
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")

# Запуск Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
