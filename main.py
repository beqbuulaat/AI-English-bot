import os
import telebot
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

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
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=json_data)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        bot.send_message(message.chat.id, reply)
    else:
        bot.send_message(message.chat.id, "⚠️ Failed to get response from AI.")

bot.polling()

# Удаляем старый webhook 
bot.remove_webhook()

# Запускаем бота в режиме long polling
bot.polling()
