# Teams Interview Bot Setup Instructions

## Prerequisites
1. Azure subscription
2. Azure OpenAI resource
3. Microsoft 365 tenant with Teams
4. Bot Framework registration

## Step 1: Azure Bot Framework Setup

### Create Bot Registration
1. Go to Azure Portal → Create Resource → Bot Channels Registration
2. Fill details:
   - Bot handle: `skysecure-interview-bot`
   - Subscription: Your subscription
   - Resource group: Create new or use existing
   - Pricing tier: F0 (Free)
3. Create Microsoft App ID and Password:
   - Go to Configuration → Manage Microsoft App ID
   - Create new app registration
   - Generate client secret
   - Save App ID and Secret

### Configure Bot Endpoint
1. In Bot registration → Configuration
2. Set Messaging endpoint: `https://your-domain.com/api/messages`
3. Enable Teams channel

## Step 2: Azure OpenAI Setup

1. Create Azure OpenAI resource
2. Deploy GPT-4 model
3. Get API key and endpoint

## Step 3: Microsoft Graph API Setup

### App Registration for Graph API
1. Azure Portal → App registrations → New registration
2. Name: `SkySecure-Graph-Access`
3. Supported account types: Single tenant
4. Register

### Configure Permissions
1. API permissions → Add permission → Microsoft Graph
2. Add these permissions:
   - `Calendars.ReadWrite` (Application)
   - `Mail.Read` (Application)
   - `User.Read` (Delegated)
3. Grant admin consent

### Generate Client Secret
1. Certificates & secrets → New client secret
2. Save the secret value

## Step 4: Environment Configuration

Create `.env` file:
```env
# Azure OpenAI
AZURE_OPENAI_KEY=your_openai_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

# Bot Framework
MICROSOFT_APP_ID=your_bot_app_id
MICROSOFT_APP_PASSWORD=your_bot_password

# Graph API (use service principal token)
GRAPH_ACCESS_TOKEN=your_graph_token
AZURE_TENANT_ID=your_tenant_id
```

## Step 5: Deploy Bot

### Local Development
```bash
pip install -r requirements_teams.txt
python app.py
```

### Production Deployment Options

#### Option 1: Azure App Service
1. Create App Service (Python 3.9+)
2. Deploy code via Git or ZIP
3. Set environment variables in Configuration
4. Update bot endpoint URL

#### Option 2: Azure Container Instances
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements_teams.txt .
RUN pip install -r requirements_teams.txt
COPY . .
EXPOSE 3978
CMD ["python", "app.py"]
```

## Step 6: Teams App Installation

### Create App Package
1. Update `manifest.json` with your bot ID
2. Add icon files (color.png, outline.png)
3. Zip manifest.json and icons

### Install in Teams
1. Teams Admin Center → Manage apps → Upload custom app
2. Upload the zip file
3. Approve and assign to users

## Step 7: Testing

### Test Commands
- "Schedule an interview at 6 PM"
- "I need to interview John for the developer position"
- "Can you set up a meeting at 6 PM today?"

### Verify Functionality
1. Bot responds to messages
2. Creates calendar events at 6 PM
3. Sends confirmation messages
4. Handles errors gracefully

## Troubleshooting

### Common Issues
1. **Bot not responding**: Check endpoint URL and credentials
2. **Calendar not created**: Verify Graph API permissions
3. **Authentication errors**: Check token expiration

### Logs
- Check Azure App Service logs
- Monitor Bot Framework channels
- Review Graph API call responses

## Security Notes
- Use managed identity in production
- Rotate secrets regularly
- Implement proper error handling
- Add rate limiting for API calls