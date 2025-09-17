from flask import Flask, request, jsonify
from outlook_agent import OutlookAgent
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
agent = OutlookAgent()

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Process with LangChain agent
        response = agent.run(user_message)
        
        return jsonify({
            "response": response,
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "agent": "OutlookAgent",
        "framework": "LangChain + LangGraph"
    })

@app.route("/api/tools", methods=["GET"])
def get_tools():
    return jsonify({
        "tools": [
            {"name": "create_meeting", "description": "Create calendar meetings"},
            {"name": "read_emails", "description": "Read recent emails"},
            {"name": "read_calendar", "description": "View calendar events"},
            {"name": "delete_meeting", "description": "Delete meetings"}
        ]
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)