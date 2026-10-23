# /RingCentral/AI/detect_intent.py
# Detect caller intent (unsubscribe, opt in, fraud, help, complaint)

python

import requests

def detect_intent(token, transcript_text):
    """
    Detect caller intent from transcript text.
    Useful for opt-in, opt-out, fraud, help, complaint, escalation.
    """
    url = "https://platform.ringcentral.com/ai/insights/v1/async/intents"

    payload = {
        "content": transcript_text,
        "language": "en-US"
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()
