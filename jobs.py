from apscheduler.schedulers.blocking import BlockingScheduler
from menu import start
from bot import Updater

sched = BlockingScheduler()
update = Updater()

@sched.scheduled_job('interval', seconds=30)
def print_interval():
    start.shed(update)

sched.start()
