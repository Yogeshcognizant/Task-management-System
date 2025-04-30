from flask import Flask
from tasks.email_remainder import send_remainder
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

def schedule_task():
    send_reminder()

scheduler = BackgroundScheduler()
scheduler.add_job(func=send_remainder, trigger="interval", hours=1)
scheduler.start()

@app.route('/')
def home():
    return "Flask server running. Sending emails every 1 hour!"

if __name__ == "__main__":
    try:
        app.run(port=5000)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
