# /code/get_campaign_mailing.py
# Paubox Marketing API
# 
# 
# 
import requests

url = "https://api.paubox.com/v1/marketing/campaign_mailings/{campaign_mailing_id}"

headers = {"authorization": "<api-key>"}

response = requests.get(url, headers=headers)

print(response.text)

# 
# HTTP 200:
# {
  "data": {
    "id": "<string>",
    "type": "campaign_mailing",
    "attributes": {
      "subject": "<string>",
      "default_subject": "<string>",
      "template_type": "<string>",
      "created_at": "2023-11-07T05:31:56Z",
      "updated_at": "2023-11-07T05:31:56Z",
      "form_data": "<string>",
      "html_part": "<string>",
      "text_part": "<string>",
      "image_data": "<string>"
    }
  }
}

# 
# HTTP 401:
# {
  "errors": [
    {
      "message": "401 Unauthorized"
    }
  ]
}

# 
# HTTP 404:
# {
  "errors": [
    {
      "message": "401 Unauthorized"
    }
  ]
}
# 
# HTTP 500:
# {
  "errors": [
    {
      "message": "401 Unauthorized"
    }
  ]
}
