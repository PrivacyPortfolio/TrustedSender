# /code/get_campaign mailings.py
# Paubox Marketing API
# Return json data about Paubox Marketing Campaign Emails
# 
# 
import requests

url = "https://api.paubox.com/v1/marketing/campaign_mailings?order=asc&items=20&page=1&pagination=true"

headers = {"authorization": "<api-key>"}

response = requests.get(url, headers=headers)

print(response.text)

# 
# HTTP 200:
{
  "data": [
    {
      "id": "<string>",
      "type": "campaign_mailing",
      "attributes": {
        "subject": "<string>",
        "default_subject": "<string>",
        "template_type": "<string>",
        "created_at": "2023-11-07T05:31:56Z",
        "updated_at": "2023-11-07T05:31:56Z",
        "sent_count": 123,
        "delivered_count": 123,
        "viewed_count": 123,
        "clicked_count": 123,
        "bounced_count": 123,
        "unsubscribed_count": 123
      }
    }
  ]
}
# 
# HTTP 400:
{
  "errors": [
    {
      "message": "401 Unauthorized"
    }
  ]
}
# 
# HTTP 401:
{
  "errors": [
    {
      "message": "401 Unauthorized"
    }
  ]
}

# 
# HTTP 500:
{
  "errors": [
    {
      "message": "401 Unauthorized"
    }
  ]
}
# 
