# /code/RingCentral/AI/transcribe_call.py
# Transcribe a call recording → text (speaker separated)

python

import requests

def transcribe_call(token, recording_id):
    """
    Submit a call recording for transcription.
    Returns a job object that can be polled for results.
    """
    url = "https://platform.ringcentral.com/ai/insights/v1/async/transcriptions"

    payload = {
        "contentUri": f"ringcentral://recording/{recording_id}",
        "encoding": "Wav",
        "language": "en-US",
        "enableSpeakerDiarization": True
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()
