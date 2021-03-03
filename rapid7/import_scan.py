from datetime import datetime
import requests
import json
import sys
import time

# Define URL for TSAC API 
import_scan_url = "https://<TSAC_FQDN>/api/v1/policies/import-scan"

# Define URL for TSAC API
login_url = "https://<TSAC_FQDN>/api/v3/users/tssa/login"
token_url = "https://<TSAC_FQDN>/api/v3/auth/tokens"

#Define headers
headers = {
  'Content-Type': 'application/json'
}

#Define payload
login_payload = {
            "authentication_method": "SRP",
            "id": "<TSAC_LOGIN>",
            "password": "<TSAC_PASSWORD>",
            "role": "BLAdmins"
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
auth_web_json_token = auth_token_response_json["json_web_token"]


# Open Token if you wish to use a manual one
#auth_web_json_token = open('/opt/bmc/rapid7/tsac-rest-python/auth.token', 'r')

#Define payload
scan_xml = sys.argv[1]
scan_xml_open = open(scan_xml, 'rb')

# Create report name
now = datetime.now()
date = now.strftime("%Y%m%d_%H%M%S")
report_name = "MANUAL-" + str(date)

#Define headers
headers = {
  'Authorization': auth_web_json_token
}

multipart_form_data = {
    'scanFile': (report_name, scan_xml_open, 'text/xml'),
    'os': ('', 'windows,linux'),
    'severities': ('','5,4,3'),
    'vendor': ('','Rapid7'),
    'cidrs': ('','')
}

#Prepare multipart/data POST request
scan_import_response = requests.post(import_scan_url, headers=headers, files=multipart_form_data ,verify=False)

scan_import_response.raise_for_status()
scan_import_response_json = scan_import_response.json()
print(scan_import_response_json)
