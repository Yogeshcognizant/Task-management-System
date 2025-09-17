import streamlit as st
import os
from outlook_agent import OutlookAgent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Outlook AI Assistant",
    page_icon="📧",
    layout="wide"
)

# Initialize agent
@st.cache_resource
def get_agent():
    return OutlookAgent()

def main():
    st.title("📧 Outlook AI Assistant")
    st.markdown("Manage your calendar and emails with natural language commands")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # Environment variables status
        st.subheader("Environment Status")
        azure_key = "✅" if os.getenv("AZURE_OPENAI_KEY") else "❌"
        azure_endpoint = "✅" if os.getenv("AZURE_OPENAI_ENDPOINT") else "❌"
        graph_token = "✅" if os.getenv("GRAPH_ACCESS_TOKEN") else "❌"
        
        st.write(f"Azure OpenAI Key: {azure_key}")
        st.write(f"Azure Endpoint: {azure_endpoint}")
        st.write(f"Graph Token: {graph_token}")
        
        st.subheader("📝 Example Commands")
        st.code("""
• Create meeting with john@company.com tomorrow at 2 PM
• Show me my recent emails
• What meetings do I have today?
• Delete my meeting with Sarah
• Schedule team sync next Monday 10 AM
        """)

    # Main chat interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Chat with Assistant")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask me to manage your calendar or emails..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get agent response
            with st.chat_message("assistant"):
                with st.spinner("Processing your request..."):
                    try:
                        agent = get_agent()
                        response = agent.run(prompt)
                        st.markdown(response)
                        
                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        error_msg = f"❌ Error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    with col2:
        st.header("🚀 Quick Actions")
        
        # Quick action buttons
        if st.button("📧 Check Emails", use_container_width=True):
            try:
                agent = get_agent()
                result = agent.read_emails("")
                st.session_state.messages.append({"role": "user", "content": "Check my emails"})
                st.session_state.messages.append({"role": "assistant", "content": result})
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        if st.button("📅 Today's Calendar", use_container_width=True):
            try:
                agent = get_agent()
                result = agent.read_calendar("")
                st.session_state.messages.append({"role": "user", "content": "Show my calendar"})
                st.session_state.messages.append({"role": "assistant", "content": result})
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        # Quick meeting form
        st.subheader("⚡ Quick Meeting")
        with st.form("quick_meeting"):
            subject = st.text_input("Meeting Subject")
            participants = st.text_input("Participants (comma-separated emails)")
            date = st.date_input("Date")
            time = st.time_input("Time")
            duration = st.number_input("Duration (minutes)", value=60, min_value=15, max_value=480)
            
            if st.form_submit_button("Create Meeting"):
                if subject and participants:
                    try:
                        # Format datetime
                        meeting_datetime = f"{date}T{time}"
                        participant_list = [email.strip() for email in participants.split(",")]
                        
                        meeting_data = {
                            "subject": subject,
                            "participants": participant_list,
                            "datetime": meeting_datetime,
                            "duration": duration
                        }
                        
                        agent = get_agent()
                        result = agent.create_meeting(str(meeting_data))
                        
                        st.session_state.messages.append({"role": "user", "content": f"Create meeting: {subject}"})
                        st.session_state.messages.append({"role": "assistant", "content": result})
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.warning("Please fill in subject and participants")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("Built with LangChain, LangGraph & Streamlit | Powered by Azure OpenAI & Microsoft Graph")

if __name__ == "__main__":
    main()