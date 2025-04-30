from flask import Flask

from apscheduler.schedulers.background import BackgroundScheduler
from tasks.email_remainder import send_remainder
import atexit

app = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.add_job(func=send_remainder, trigger="interval", hours=5)
scheduler.start()

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()

atexit.register(shutdown_scheduler)
@app.route('/')
def index():
    return "Flask server running. Sending emails every 1 hour!"

if __name__ == "__main__":
    app.run(debug=True, port=5001)
    
