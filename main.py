import os
import telebot
from flask import Flask, render_template

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TOKEN or not CHAT_ID:
    raise ValueError("Не установлены переменные TELEGRAM_TOKEN и CHAT_ID")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

last_status = "Бот запущен"
last_check = "Проверка ещё не выполнялась"

@app.route("/")
def status():
    return render_template("status.html", status=last_status, check_time=last_check)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Бот успешно запущен и работает!")

if __name__ == "__main__":
    bot.remove_webhook()
    while True:
        try:
            bot.polling(none_stop=True, interval=1)
        except Exception as e:
            print(f"Ошибка polling: {e}")
