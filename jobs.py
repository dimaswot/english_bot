from apscheduler.schedulers.blocking import BlockingScheduler
from menu import start

sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=30)
def print_interval():
    start.shed()
    print("=="*20)

sched.start()
