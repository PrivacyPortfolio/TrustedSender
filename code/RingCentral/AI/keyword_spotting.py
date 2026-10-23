# /code/RingCentral/AI/keyword_spotting.py
# Spot keywords (STOP, START, HELP, UNSUBSCRIBE)

python

import requests

def keyword_spotting(token, transcript_text):
    """
    Spot keyphrases such as STOP, START, HELP, UNSUBSCRIBE.
    Critical for TrustedSender consent workflows.
    """
    url = "https://platform.ringcentral.com/ai/insights/v1/async/keyphrases"

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
