from flask import Flask, request, Response
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.schema import Activity
from teams_bot import TeamsInterviewBot
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Bot Framework Adapter Settings
SETTINGS = BotFrameworkAdapterSettings(
    app_id=os.getenv("MICROSOFT_APP_ID"),
    app_password=os.getenv("MICROSOFT_APP_PASSWORD")
)

# Create adapter and bot
ADAPTER = BotFrameworkAdapter(SETTINGS)
BOT = TeamsInterviewBot()

@app.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = request.headers["Authorization"] if "Authorization" in request.headers else ""

    async def aux_func(turn_context):
        await BOT.on_message_activity(turn_context)

    try:
        task = ADAPTER.process_activity(activity, auth_header, aux_func)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(task)
        return Response(status=200)
    except Exception as e:
        print(f"Error: {e}")
        return Response(status=500)

@app.route("/", methods=["GET"])
def health_check():
    return {"status": "Teams Interview Bot is running!", "version": "1.0"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3978, debug=True)