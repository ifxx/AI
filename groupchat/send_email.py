# filename: send_email.py

import requests
import os

# Get the summary from the previous step
summary = os.environ.get('SUMMARY')

# Get the token
token = os.environ.get('GRAPH_TOKEN')

# Set the headers
headers = {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
}

# Set the body
body = {
    "message": {
        "subject": "Summary of the webpage",
        "body": {
            "contentType": "Text",
            "content": summary
        },
        "toRecipients": [
            {
                "emailAddress": {
                    "address": "kylino@hotmail.com"
                }
            }
        ]
    },
    "saveToSentItems": "true"
}

# Send the request
response = requests.post('https://graph.microsoft.com/v1.0/me/sendMail', headers=headers, json=body)

# Print the response
print(response.status_code)