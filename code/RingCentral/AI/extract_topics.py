# /code/RingCentral/AI/extract_topics.py
# Extract topics (billing, medical, legal, support, marketing)

python

import requests

def extract_topics(token, transcript_text):
    """
    Extract topics from transcript text.
    Useful for routing calls to the correct Yo-AI agent.
    """
    url = "https://platform.ringcentral.com/ai/insights/v1/async/topics"

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
