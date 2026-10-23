# /code/RingCentral/AI/analyze_sentiment.py
# Analyze emotional tone of a transcript

python

import requests

def analyze_sentiment(token, transcript_text):
    """
    Analyze sentiment (positive, negative, neutral) for a transcript.
    """
    url = "https://platform.ringcentral.com/ai/insights/v1/async/sentiment"

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
