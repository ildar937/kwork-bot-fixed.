import telebot
from flask import Flask, render_template
import os
from datetime import datetime

TOKEN = os.environ.get('BOT_TOKEN', 'YOUR_TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID', 'YOUR_CHAT_ID')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

last_status = "Bot starting..."
last_check = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.route('/')
def status():
    return render_template("status.html", status=last_status, check_time=last_check)

# Очистка вебхука перед запуском long polling
bot.delete_webhook()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Bot is running ✅")

def run_bot():
    global last_status, last_check
    last_status = "Bot running..."
    last_check = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bot.polling(none_stop=True)

if __name__ == "__main__":
    from threading import Thread
    Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=3000)
