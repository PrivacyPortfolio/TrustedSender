# /code/send_campaign_mailings.py
# Paubox Marketing API
# Send campaign email to recipients.
# 
# 
import requests

url = "https://api.paubox.com/v1/marketing/campaign_mailing_sends"

payload = {
    "campaign_mailing_id": "g79da293-4a84-4b50-b0d9-76a16af167fe",
    "campaign_mailing_send": {
        "sender_email": "marketing@yourdomain.com",
        "subscription_list_id": "1a55ec71-0b08-457a-b183-51ac7791f1fe",
        "recipient_emails": ["test1@example.com", "test2@example.com"],
        "from_email": "no-reply@yourdomain.com",
        "from_name": "Your Company Name",
        "subject": "Your Campaign Subject"
    }
}
headers = {
    "authorization": "<api-key>",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)

# 
# HTTP 200:
# {}

# HTTP 400:
# {
  "errors": [
    {
      "message": "401 Unauthorized"
    }
  ]
}

# HTTP 401:
# # {
  "errors": [
    {
      "message": "401 Unauthorized"
    }
  ]
}

# HTTP 422:
# # {
  "errors": [
    {
      "message": "401 Unauthorized"
    }
  ]
}

# HTTP 500:
# # {
  "errors": [
    {
      "message": "401 Unauthorized"
    }
  ]
}

