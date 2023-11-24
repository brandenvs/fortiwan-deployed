import requests, json
from django.conf import settings
from decouple import config, Csv
import os

# GET BEARER TOKEN
def get_token(request):
    """Obtain a Bearer Token for authenticated requests.

    This function sends a POST request to the Fortinet authentication API
    to retrieve a Bearer Token for subsequent authenticated API calls.

    :param request: The request object, typically from a Django web framework view.
                    It is used to check if the user is authenticated.
    
    :return: A Bearer Token string if authentication is successful, otherwise None.

    :raises: Exception if an unexpected error occurs during the API call."""
    flag = False
    bearer_token = None

    if request.user.is_authenticated:
        # Session Persists & Connection Pooling
        session = requests.Session() 
        # Session Verification & Tracking
        session.verify = True # Verification
        session.trust_env = False # Tracking

        # Base URL
        auth_url = "https://customerapiauth.fortinet.com/api/v1/oauth/token/"

        # Payload Variables
        api_key = settings.API_KEY
        password = settings.PASSWORD
        client_id = settings.CLIENT_ID
        print(f'{api_key} || {password} || {client_id}')

        # Request Headers
        headers = {
            'Content-Type': 'application/json',
        }

        # Define Payload
        payload = {
            'username': api_key,
            'password': password,
            'client_id': client_id,
            'grant_type': 'password',
        }               
        
        # Call API: POST
        try:
            response = session.request('post', auth_url, headers=headers, json=payload, verify=False)
            if response.status_code == 200:
                # Print Response
                print(f'RESPONSE: {response.json()}')                
                try:
                    # Extract Bearer Token
                    bearer_token = response.json()['access_token']
                    # Update Flag
                    flag = True
                except:
                    print('[ERROR] Could Not Extract a Bearer Token...')
        except Exception as e:
            print(f"Unexpected Error: {e}")
    
    # Update Environment Variable
    if bearer_token:
        os.environ['BEARER_TOKEN'] = bearer_token