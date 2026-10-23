# campaigns/Email_Migration/WorkMailForwarder_lambda.py
# 
# environmental variables:  PAUBOX_API_KEY = <your Paubox API key>
# 
# Paubox API URL: Replace: https://api.paubox.net/v1/yourdomain/messages
# with your actual Paubox domain endpoint.
# 
# WorkMail Inbound Rule
# Your rule should:
# •	Trigger this Lambda
# •	Only when subject contains "Quarantine Report" or "DLP Notification"
# 
# WorkMail will pass:
# {
#  "messageId": "...",
#  "organizationId": "..."
# }

# What This Function Does
# •	Pulls the raw MIME message from WorkMail
# •	Parses subject, sender, and body
# •	Sends a new email through Paubox to the Paubox Administrator (Paubox user with admin rights)
# •	Preserves HTML formatting
# •	Works with encrypted inbound mail (Paubox handles encryption on send)

import boto3
import os
import json
import base64
import requests
from email import message_from_bytes

PAUBOX_API_KEY = os.environ["PAUBOX_API_KEY"]
PAUBOX_API_URL = "https://api.paubox.net/v1/yourdomain/messages"  # Replace "yourdomain"
PAUBOX_ADMIN_EMAIL = "pauboxadminuser@pauboxcustomer.com"    # Replace "pauboxadminuser@pauboxcustomer.com"

def lambda_handler(event, context):
    # WorkMail inbound event contains messageId and organizationId
    message_id = event["messageId"]
    org_id = event["organizationId"]

    workmail = boto3.client("workmailmessageflow")

    # 1. Retrieve raw MIME email
    raw_msg = workmail.get_raw_message_content(
        messageId=message_id
    )["messageContent"].read()

    msg = message_from_bytes(raw_msg)

    # Extract subject and body
    subject = msg.get("Subject", "(no subject)")
    from_addr = msg.get("From")
    to_addr = PAUBOX_ADMIN_EMAIL

    # Extract body (prefer HTML)
    body = None
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == "text/html":
                body = part.get_payload(decode=True).decode(errors="ignore")
                break
            if ctype == "text/plain" and body is None:
                body = part.get_payload(decode=True).decode(errors="ignore")
    else:
        body = msg.get_payload(decode=True).decode(errors="ignore")

    # 2. Build Paubox API payload
    payload = {
        "from": from_addr,
        "to": [to_addr],
        "subject": subject,
        "html_body": body,
        "force_secure_notification": False
    }

    # 3. Send via Paubox Email API
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": PAUBOX_API_KEY
    }

    response = requests.post(PAUBOX_API_URL, headers=headers, data=json.dumps(payload))

    # Log for debugging
    print("Paubox response:", response.status_code, response.text)

    return {
        "statusCode": response.status_code,
        "body": response.text
    }
