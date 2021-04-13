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

token = "1794885741:AAGBtWvALZjTzw1WDefzwSCie9ScpHmdHL0" #os.getenv("TOKEN") #
url = "https://e429ff1617fe.ngrok.io"

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


