import os
import requests
from azure.identity import ClientSecretCredential
from datetime import datetime, timedelta

class GraphAuthHelper:
    def __init__(self):
        self.tenant_id = os.getenv("AZURE_TENANT_ID")
        self.client_id = os.getenv("MICROSOFT_APP_ID")
        self.client_secret = os.getenv("MICROSOFT_APP_PASSWORD")
        self.scope = "https://graph.microsoft.com/.default"
        
    def get_access_token(self):
        """Get access token for Microsoft Graph API using client credentials flow"""
        try:
            credential = ClientSecretCredential(
                tenant_id=self.tenant_id,
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            
            token = credential.get_token(self.scope)
            return token.token
            
        except Exception as e:
            print(f"Error getting access token: {e}")
            return None
    
    def get_token_via_rest(self):
        """Alternative method using REST API directly"""
        try:
            url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
            
            data = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': self.scope
            }
            
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                return response.json().get('access_token')
            else:
                print(f"Token request failed: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error in REST token request: {e}")
            return None

# Usage example for testing
if __name__ == "__main__":
    auth = GraphAuthHelper()
    token = auth.get_access_token()
    
    if token:
        print("✅ Successfully obtained access token")
        print(f"Token starts with: {token[:20]}...")
    else:
        print("❌ Failed to get access token")
        print("Check your environment variables and Azure app registration")