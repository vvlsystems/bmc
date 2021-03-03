import requests
import json

# Define URL for TSAC API 
login_url = "https://<TSAC_FQDN>/api/v3/users/tssa/login"
token_url = "https://<TSAC_FQDN>/api/v3/auth/tokens"

#Define payload
login_payload = {  
            "authentication_method": "SRP", 
            "id": "<TSAC_LOGIN>", 
            "password": "<TSAC_PASSWORD>",
            "role": "BLAdmins" 
          }

#Define headers
headers = {
  'Content-Type': 'application/json'
}

# Authenticate to get token
auth_response = requests.post(login_url, headers=headers, json=login_payload, verify=False)
auth_response.raise_for_status()
auth_response_json = auth_response.json()

#print(auth_response_json)
auth_token = auth_response_json["token"]

# Refresh Token
token_payload = {
                 "context": {
                 },
                 "refresh_token": auth_token
                 }

auth_token_response = requests.post(token_url, headers=headers, json=token_payload, verify=False)
auth_token_response.raise_for_status()
auth_token_response_json = auth_token_response.json()
#print(auth_token_response_json)

auth_web_json_token = auth_token_response_json["json_web_token"]
#print(auth_web_json_token)
token_file = open('auth.token', 'w+')
token_file.write(auth_web_json_token)
token_file.close()
