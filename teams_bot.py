from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from botbuilder.schema import ChannelAccount, Activity, ActivityTypes
from datetime import datetime, timedelta
import json
import os
import requests
from openai import AzureOpenAI
from auth_helper import GraphAuthHelper

class TeamsInterviewBot(ActivityHandler):
    def __init__(self):
        # Azure OpenAI configuration
        self.azure_openai_client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version="2024-02-01",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        
        # Graph API authentication
        self.auth_helper = GraphAuthHelper()
        self.graph_token = None
        self._refresh_token()
    
    def _refresh_token(self):
        """Refresh the Graph API access token"""
        self.graph_token = self.auth_helper.get_access_token()
        if not self.graph_token:
            print("Warning: Could not obtain Graph API token")
    
    def _get_headers(self):
        """Get headers with fresh token"""
        if not self.graph_token:
            self._refresh_token()
        
        return {
            "Authorization": f"Bearer {self.graph_token}",
            "Content-Type": "application/json"
        }
        
    async def on_message_activity(self, turn_context: TurnContext):
        user_message = turn_context.activity.text.lower()
        
        # Check if user wants to schedule an interview
        if any(keyword in user_message for keyword in ["interview", "schedule", "meeting", "6 pm", "6pm"]):
            await self._handle_interview_scheduling(turn_context, user_message)
        else:
            # General chat response
            response = await self._get_ai_response(user_message)
            await turn_context.send_activity(MessageFactory.text(response))
    
    async def _handle_interview_scheduling(self, turn_context: TurnContext, message: str):
        try:
            # Extract interview details using AI
            interview_details = await self._extract_interview_details(message)
            
            # Schedule at 6 PM today or tomorrow
            interview_time = self._get_6pm_slot()
            
            # Create calendar event
            meeting_result = await self._create_interview_meeting(
                interview_details, 
                interview_time,
                turn_context.activity.from_property.name
            )
            
            if meeting_result["success"]:
                response = f"✅ Interview scheduled for {interview_time.strftime('%B %d at 6:00 PM')}!\n\n" \
                          f"📋 Details:\n" \
                          f"• Candidate: {interview_details.get('candidate', 'TBD')}\n" \
                          f"• Position: {interview_details.get('position', 'TBD')}\n" \
                          f"• Duration: 60 minutes\n\n" \
                          f"📧 Calendar invite sent!"
            else:
                response = f"❌ Failed to schedule interview: {meeting_result['error']}"
                
        except Exception as e:
            response = f"❌ Error scheduling interview: {str(e)}"
        
        await turn_context.send_activity(MessageFactory.text(response))
    
    async def _extract_interview_details(self, message: str):
        prompt = f"""
        Extract interview details from this message: "{message}"
        
        Return JSON with:
        - candidate: candidate name (if mentioned)
        - position: job position (if mentioned)
        - interviewer: interviewer name (if mentioned)
        
        If not mentioned, use "TBD" as default.
        """
        
        response = self.azure_openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except:
            return {"candidate": "TBD", "position": "TBD", "interviewer": "TBD"}
    
    def _get_6pm_slot(self):
        now = datetime.now()
        today_6pm = now.replace(hour=18, minute=0, second=0, microsecond=0)
        
        # If it's already past 6 PM today, schedule for tomorrow
        if now >= today_6pm:
            return today_6pm + timedelta(days=1)
        else:
            return today_6pm
    
    async def _create_interview_meeting(self, details, interview_time, requester):
        try:
            end_time = interview_time + timedelta(hours=1)
            
            event = {
                "subject": f"Interview - {details.get('candidate', 'Candidate')} for {details.get('position', 'Position')}",
                "body": {
                    "contentType": "HTML",
                    "content": f"""
                    <h3>Interview Details</h3>
                    <p><strong>Candidate:</strong> {details.get('candidate', 'TBD')}</p>
                    <p><strong>Position:</strong> {details.get('position', 'TBD')}</p>
                    <p><strong>Requested by:</strong> {requester}</p>
                    <p><strong>Duration:</strong> 60 minutes</p>
                    """
                },
                "start": {
                    "dateTime": interview_time.isoformat(),
                    "timeZone": "UTC"
                },
                "end": {
                    "dateTime": end_time.isoformat(),
                    "timeZone": "UTC"
                },
                "attendees": [
                    {
                        "emailAddress": {
                            "address": "hr@company.com",  # Replace with actual HR email
                            "name": "HR Team"
                        },
                        "type": "required"
                    }
                ],
                "isOnlineMeeting": True,
                "onlineMeetingProvider": "teamsForBusiness"
            }
            
            headers = self._get_headers()
            
            response = requests.post(
                "https://graph.microsoft.com/v1.0/me/events",
                headers=headers,
                json=event
            )
            
            if response.status_code == 201:
                return {"success": True, "event_id": response.json().get("id")}
            else:
                return {"success": False, "error": response.text}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _get_ai_response(self, message: str):
        try:
            response = self.azure_openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful Teams bot assistant. Be friendly and concise. If someone mentions scheduling interviews or meetings, offer to help schedule them at 6 PM."
                    },
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"I'm having trouble processing that right now. Error: {str(e)}"
    
    async def on_members_added_activity(self, members_added: [ChannelAccount], turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                welcome_message = """
                👋 Hi! I'm your interview scheduling assistant!
                
                I can help you:
                • Schedule interviews at 6 PM
                • Create calendar events
                • Answer questions
                
                Just mention "schedule interview" or "6 PM" and I'll help you set it up!
                """
                await turn_context.send_activity(MessageFactory.text(welcome_message))