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
from user_bd import Session, Word


token =  os.getenv("TOKEN") #"1794885741:AAGBtWvALZjTzw1WDefzwSCie9ScpHmdHL0"
url = "https://english1bot.herokuapp.com/"

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

@app.route("/words")
def give_words():
    str = ''
    session = Session()
    all_words = session.query(Word).all()
    for word in all_words:
        str += f'{word.word}\n'
    return f'{str}'


