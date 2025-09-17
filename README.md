# Teams Interview Scheduler Bot 🤖

An AI-powered Microsoft Teams bot that automatically schedules interviews at 6 PM when mentioned in chat conversations.

## Features ✨

- **Smart Interview Detection**: Recognizes when users want to schedule interviews
- **Automatic 6 PM Scheduling**: Always schedules interviews at 6:00 PM (today or tomorrow)
- **AI-Powered Extraction**: Uses Azure OpenAI to extract candidate and position details
- **Calendar Integration**: Creates Outlook calendar events with Teams meeting links
- **Natural Language**: Responds to casual conversation about scheduling

## Quick Start 🚀

### 1. Clone and Setup
```bash
git clone <your-repo>
cd skysecure
cp .env.example .env
```

### 2. Configure Environment Variables
Edit `.env` file with your Azure credentials:
```env
AZURE_OPENAI_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
MICROSOFT_APP_ID=your_bot_app_id
MICROSOFT_APP_PASSWORD=your_bot_password
AZURE_TENANT_ID=your_tenant_id
```

### 3. Deploy and Run
```bash
python deploy.py
```

## Usage Examples 💬

The bot responds to these types of messages in Teams:

- "I need to schedule an interview at 6 PM"
- "Can we interview John for the developer position?"
- "Schedule interview with Sarah tomorrow"
- "Set up a 6 PM meeting for candidate review"

## Architecture 🏗️

```
Teams Chat → Bot Framework → Flask App → Azure OpenAI + Graph API → Calendar Event
```

### Components:
- **teams_bot.py**: Main bot logic and message handling
- **app.py**: Flask webhook server
- **auth_helper.py**: Microsoft Graph authentication
- **deploy.py**: Automated deployment script

## Azure Services Used ☁️

1. **Azure OpenAI**: GPT-4 for natural language processing
2. **Azure Bot Service**: Teams bot registration and channels
3. **Microsoft Graph API**: Calendar and email integration
4. **Azure App Service**: Bot hosting (optional)

## Development Setup 🛠️

### Prerequisites
- Python 3.9+
- Azure subscription
- Microsoft 365 tenant
- Teams admin access

### Local Development
```bash
pip install -r requirements_teams.txt
python app.py
```

Bot runs on `http://localhost:3978`

### Testing
Use Bot Framework Emulator or ngrok for local testing:
```bash
ngrok http 3978
```

## Deployment Options 📦

### Option 1: Azure App Service
- Automatic scaling
- Built-in monitoring
- Easy CI/CD integration

### Option 2: Azure Container Instances
- Containerized deployment
- Cost-effective for low traffic
- Quick setup

### Option 3: Local/On-Premises
- Full control
- Custom networking
- Requires public endpoint

## Security 🔒

- Uses Azure Managed Identity in production
- Implements proper token refresh
- Validates bot framework signatures
- Encrypts sensitive data in transit

## Troubleshooting 🔧

### Common Issues:

**Bot not responding:**
- Check webhook URL in Bot Framework
- Verify app ID and password
- Test endpoint accessibility

**Calendar events not created:**
- Verify Graph API permissions
- Check token expiration
- Confirm tenant configuration

**Authentication errors:**
- Validate Azure app registration
- Check client secret expiration
- Verify tenant ID

### Logs and Monitoring:
- Azure Application Insights
- Bot Framework Analytics
- Custom logging in Flask app

## Contributing 🤝

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

## License 📄

MIT License - see LICENSE file for details

## Support 💬

For issues and questions:
- Create GitHub issue
- Check setup_instructions.md for detailed configuration
- Review Azure documentation for service-specific help