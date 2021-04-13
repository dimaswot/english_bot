from apscheduler.schedulers.blocking import BlockingScheduler
from menu import start
from user_bd import Session, User
from app import bot

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=30)
def print_interval():
    print("ПРОИЗОШЛО НАПОМИНАНИЕ")
    session = Session()
    users = session.query(User).all()
    for user in users:
        start.shed(bot, user)

sched.start()
