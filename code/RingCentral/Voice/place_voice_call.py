# /code/RingCentral/place_voice_call.py
# Initiate outbound voice calls (voice opt in/opt out)

python

import requests

def place_voice_call(account_id, extension_id, token, to_number, from_number):
    url = f"https://platform.ringcentral.com/restapi/v1.0/account/{account_id}/extension/{extension_id}/ring-out"

    payload = {
        "to": {"phoneNumber": to_number},
        "from": {"phoneNumber": from_number},
        "playPrompt": True
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()
