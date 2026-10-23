# /code/RingCentral/send_sms_message.py
# Send SMS (opt in, opt out, confirmation, registration)
python

import requests

def send_sms_message(account_id, extension_id, token, to_number, from_number, text):
    url = f"https://platform.ringcentral.com/restapi/v1.0/account/{account_id}/extension/{extension_id}/sms"

    payload = {
        "to": [{"phoneNumber": to_number}],
        "from": {"phoneNumber": from_number},
        "text": text
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()
