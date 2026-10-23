# /code/RingCentral/subscribe_sms_events.py
# Subscribe to SMS events (STOP, START, HELP, inbound SMS)

python

import requests

def subscribe_sms_events(token, event_filters, delivery_address):
    url = "https://platform.ringcentral.com/restapi/v1.0/subscription"

    payload = {
        "eventFilters": event_filters,
        "deliveryMode": {
            "transportType": "Webhook",
            "address": delivery_address
        }
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()
