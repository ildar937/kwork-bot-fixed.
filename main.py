import os
from flask import Flask, request, render_template
import telebot
from dotenv import load_dotenv

# 1) Загружаем переменные из .env
load_dotenv()
TOKEN   = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
HEROKU_APP_URL = os.getenv("HEROKU_APP_URL")  # например, https://your-app.herokuapp.com

if not TOKEN or not CHAT_ID or not HEROKU_APP_URL:
    raise RuntimeError("Не установлены TELEGRAM_TOKEN, CHAT_ID или HEROKU_APP_URL")

# 2) Инициализируем бота и Flask
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__, template_folder="templates")

# 3) Ставим webhook один раз при первом запросе
@app.before_first_request
def setup_webhook():
    bot.remove_webhook()
    webhook = f"{HEROKU_APP_URL}/webhook/{TOKEN}"
    bot.set_webhook(url=webhook)

# 4) Статус-страница
@app.route("/")
def status():
    return render_template("status.html")

# 5) Приём обновлений от Telegram
@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def telegram_webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "", 200

# 6) Обработчик команды /start
@bot.message_handler(commands=['start'])
def on_start(message):
    bot.send_message(message.chat.id, "Бот запущен и готов принимать заявки!")

# 7) Приём формы и отправка в Telegram
@app.route("/submit", methods=["POST"])
def handle_form():
    data = request.form
    text = (
        f"🆕 *Новая заявка*\n"
        f"👤 Имя: {data.get('name')}\n"
        f"✉️ Telegram: {data.get('telegram')}\n"
        f"📋 Тема: {data.get('topic')}\n"
        f"📱 Телефон: {data.get('phone') or '–'}\n\n"
        f"💬 Сообщение:\n{data.get('message')}"
    )
    bot.send_message(CHAT_ID, text, parse_mode="Markdown")
    return render_template("thank-you.html")

# 8) Запуск
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
