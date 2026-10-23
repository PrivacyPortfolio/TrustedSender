# /code/RingCentral/unsubscribe_sms_events.py
# Unsubscribe from SMS event notifications

python

import requests

def unsubscribe_sms_events(subscription_id, token):
    url = f"https://platform.ringcentral.com/restapi/v1.0/subscription/{subscription_id}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.delete(url, headers=headers)
    return response.json()
