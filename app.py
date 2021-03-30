from flask import Flask, request
import requests
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, CallbackContext, Filters, CallbackQueryHandler
import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
import states
from apscheduler.schedulers.blocking import BlockingScheduler
from bot import TelBot
from user import User
from datetime import timedelta

token = "1693338559:AAFniq64i8lKTKVWjGdq9_9lDki1W4SK3X8"
url = "https://9c736311012c.ngrok.io"
CHAT_ID = 742632933

app = Flask(__name__)
bot = TelBot(token)

@app.route("/", methods=["GET", "POST"])
def receive_update():
    bot.update(request.json)
    return {"ok": True}

@app.route("/webhook")
def set_webhook():
    bot.updater.bot.set_webhook(
        f'{url}/{token}'
    )
    return 'ok'


