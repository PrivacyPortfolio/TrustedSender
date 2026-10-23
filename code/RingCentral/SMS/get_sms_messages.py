# /RingCentral/get_sms_messages.py
# Retrieve inbound SMS (STOP, START, HELP, registration replies)

python

import requests

def get_sms_messages(account_id, extension_id, token, message_type="SMS"):
    url = f"https://platform.ringcentral.com/restapi/v1.0/account/{account_id}/extension/{extension_id}/message-store"

    params = {"messageType": message_type}

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, params=params, headers=headers)
    return response.json()
