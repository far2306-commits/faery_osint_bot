import telebot
import requests
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")  # ambil dari env Render
NUMVERIFY_API = os.environ.get("NUMVERIFY_API")  # ambil dari env

bot = telebot.TeleBot(BOT_TOKEN)

# Handler start & message (sama kaya sebelumnya)
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "CRPT.ZDX OSINT BOT SIAP NGEWEK NOMOR HP LU 😈🔥\nKirim nomor +62xxxxxxxxxx kontol!")

@bot.message_handler(func=lambda message: True)
def cek_nomor(message):
    nomor = message.text.strip()
    if not nomor.startswith('+'):
        nomor = '+' + nomor.lstrip('0')

    bot.reply_to(message, f"Lagi ngecek {nomor}... sabar anjing 🔥")

    try:
        url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_API}&number={nomor}&format=1"
        r = requests.get(url).json()
        if r.get("valid"):
            respon = f"✅ VALID BANG 😈\nNomor: {r.get('international_format')}\nNegara: {r.get('country_name')}\nLokasi: {r.get('location', 'Ga ketauan')}\nOperator: {r.get('carrier', 'Rahasia')}"
        else:
            respon = "Nomor ga valid kontol!"
    except:
        respon = "API error jahanam 🦠"

    bot.reply_to(message, respon)

# Webhook setup
import flask
from flask import request

app = flask.Flask(__name__)

@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'OK', 200

@app.route('/')
def index():
    return "Bot CRPT.ZDX jalan anjing! 🔥"

if __name__ == "__main__":
    # Buat webhook pas start (Render kasih URL otomatis)
    bot.remove_webhook()
    webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{BOT_TOKEN}"
    bot.set_webhook(url=webhook_url)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
