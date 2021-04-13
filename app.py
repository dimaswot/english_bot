from flask import Flask, request
import requests
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, CallbackContext, Filters, CallbackQueryHandler
import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
import states
from apscheduler.schedulers.blocking import BlockingScheduler
from bot import TelBot
from datetime import timedelta
import os

<<<<<<< HEAD
token =  os.getenv("TOKEN") #"1794885741:AAGBtWvALZjTzw1WDefzwSCie9ScpHmdHL0"
url = "https://e429ff1617fe.ngrok.io"
=======
token = "1693338559:AAFniq64i8lKTKVWjGdq9_9lDki1W4SK3X8"
url = "https://english1bot.herokuapp.com/"
CHAT_ID = 742632933
>>>>>>> ad061af1c22163f96e28023a8e80582304a5268f

app = Flask(__name__)
bot = TelBot(token)

@app.route(f"/{token}", methods=["GET", "POST"])
def receive_update():
    bot.update(request.json)
    return {"ok": True}

@app.route("/webhook")
def set_webhook():
    bot.updater.bot.set_webhook(
        f'{url}/{token}'
    )
    return 'ok'
