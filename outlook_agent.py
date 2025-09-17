from langchain.agents import Tool, AgentExecutor, create_openai_functions_agent
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
import requests
import json
import os
from datetime import datetime, timedelta

# Configuration
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
GRAPH_ACCESS_TOKEN = os.getenv("GRAPH_ACCESS_TOKEN")

class AgentState(TypedDict):
    messages: List[dict]
    user_input: str
    result: str

class OutlookAgent:
    def __init__(self):
        self.llm = AzureChatOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_KEY,
            api_version="2024-02-01",
            deployment_name="gpt-4",
            temperature=0.1
        )
        
        self.tools = [
            Tool(
                name="create_meeting",
                description="Create a calendar meeting. Input: JSON with subject, participants, datetime, duration",
                func=self.create_meeting
            ),
            Tool(
                name="read_emails",
                description="Read recent emails from inbox",
                func=self.read_emails
            ),
            Tool(
                name="read_calendar",
                description="Read today's calendar events",
                func=self.read_calendar
            ),
            Tool(
                name="delete_meeting",
                description="Delete a meeting by subject. Input: meeting subject",
                func=self.delete_meeting
            )
        ]
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an Outlook assistant. Help users manage their calendar and emails.
            
            Available tools:
            - create_meeting: Create calendar events
            - read_emails: View recent emails
            - read_calendar: View today's meetings
            - delete_meeting: Delete meetings
            
            Always use tools to perform actions. Be helpful and concise."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        self.agent = create_openai_functions_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)
        
        # Create LangGraph workflow
        self.workflow = self.create_workflow()

    def create_meeting(self, input_str: str) -> str:
        try:
            # Parse input or use LLM to extract details
            if isinstance(input_str, str) and not input_str.startswith('{'):
                # Use LLM to extract meeting details
                extraction_prompt = f"""
                Extract meeting details from: "{input_str}"
                Return JSON: {{"subject": "...", "participants": ["email"], "datetime": "ISO format", "duration": 60}}
                """
                response = self.llm.invoke(extraction_prompt)
                meeting_data = json.loads(response.content)
            else:
                meeting_data = json.loads(input_str)
            
            # Default datetime if not provided
            if not meeting_data.get("datetime"):
                tomorrow = datetime.now() + timedelta(days=1)
                meeting_data["datetime"] = tomorrow.replace(hour=14, minute=0, second=0).isoformat()
            
            event = {
                "subject": meeting_data.get("subject", "Meeting"),
                "start": {"dateTime": meeting_data["datetime"], "timeZone": "UTC"},
                "end": {"dateTime": (datetime.fromisoformat(meeting_data["datetime"]) + timedelta(minutes=meeting_data.get("duration", 60))).isoformat(), "timeZone": "UTC"},
                "attendees": [{"emailAddress": {"address": email}, "type": "required"} for email in meeting_data.get("participants", [])]
            }
            
            headers = {"Authorization": f"Bearer {GRAPH_ACCESS_TOKEN}", "Content-Type": "application/json"}
            response = requests.post("https://graph.microsoft.com/v1.0/me/events", headers=headers, json=event)
            
            if response.status_code == 201:
                return f"✅ Meeting created: {meeting_data.get('subject', 'Meeting')}"
            else:
                return f"❌ Failed to create meeting: {response.text}"
                
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def read_emails(self, input_str: str = "") -> str:
        try:
            headers = {"Authorization": f"Bearer {GRAPH_ACCESS_TOKEN}", "Content-Type": "application/json"}
            response = requests.get("https://graph.microsoft.com/v1.0/me/messages?$top=5&$select=subject,from,isRead", headers=headers)
            
            if response.status_code == 200:
                emails = response.json().get("value", [])
                if not emails:
                    return "📧 No emails found"
                
                result = "📧 Recent Emails:\n"
                for email in emails:
                    status = "🔵" if not email.get("isRead") else "⚪"
                    sender = email.get("from", {}).get("emailAddress", {}).get("name", "Unknown")
                    subject = email.get("subject", "No subject")
                    result += f"{status} {sender}: {subject}\n"
                
                return result
            else:
                return f"❌ Failed to read emails: {response.text}"
                
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def read_calendar(self, input_str: str = "") -> str:
        try:
            headers = {"Authorization": f"Bearer {GRAPH_ACCESS_TOKEN}", "Content-Type": "application/json"}
            today = datetime.now().isoformat()
            tomorrow = (datetime.now() + timedelta(days=1)).isoformat()
            
            response = requests.get(f"https://graph.microsoft.com/v1.0/me/calendarview?startDateTime={today}&endDateTime={tomorrow}", headers=headers)
            
            if response.status_code == 200:
                events = response.json().get("value", [])
                if not events:
                    return "📅 No meetings today"
                
                result = "📅 Today's Meetings:\n"
                for event in events:
                    subject = event.get("subject", "No subject")
                    start_time = event.get("start", {}).get("dateTime", "")
                    if start_time:
                        time_obj = datetime.fromisoformat(start_time.replace('Z', ''))
                        time_str = time_obj.strftime("%I:%M %p")
                        result += f"🕐 {time_str}: {subject}\n"
                
                return result
            else:
                return f"❌ Failed to read calendar: {response.text}"
                
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def delete_meeting(self, subject: str) -> str:
        try:
            headers = {"Authorization": f"Bearer {GRAPH_ACCESS_TOKEN}", "Content-Type": "application/json"}
            response = requests.get(f"https://graph.microsoft.com/v1.0/me/events?$filter=contains(subject,'{subject}')", headers=headers)
            
            if response.status_code == 200:
                events = response.json().get("value", [])
                if not events:
                    return f"❌ No meeting found with subject: {subject}"
                
                event_id = events[0].get("id")
                delete_response = requests.delete(f"https://graph.microsoft.com/v1.0/me/events/{event_id}", headers=headers)
                
                if delete_response.status_code == 204:
                    return f"✅ Meeting deleted: {events[0].get('subject')}"
                else:
                    return f"❌ Failed to delete meeting: {delete_response.text}"
            else:
                return f"❌ Failed to search meetings: {response.text}"
                
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def create_workflow(self):
        workflow = StateGraph(AgentState)
        
        def process_input(state: AgentState):
            user_input = state["user_input"]
            result = self.agent_executor.invoke({"input": user_input, "chat_history": []})
            return {"result": result["output"]}
        
        workflow.add_node("process", process_input)
        workflow.set_entry_point("process")
        workflow.add_edge("process", END)
        
        return workflow.compile()

    def run(self, user_input: str) -> str:
        state = {"user_input": user_input, "messages": [], "result": ""}
        result = self.workflow.invoke(state)
        return result["result"]