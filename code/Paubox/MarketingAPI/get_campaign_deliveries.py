# /code/get_campaign_deliveries.py
# Paubox Marketing API
# Returns json data about campaign deliveries sent
# 
import requests

url = "https://api.paubox.com/v1/marketing/analytics/campaign_mailing_deliveries_table"

headers = {"authorization": "<api-key>"}

response = requests.get(url, headers=headers)

print(response.text)
# 
# HTTP 200:
{
  "data": [
    {
      "first_name": "<string>",
      "last_name": "<string>",
      "recipient_email": "<string>",
      "created_at": "2023-11-07T05:31:56Z",
      "delivered": "2023-11-07T05:31:56Z",
      "viewed": "2023-11-07T05:31:56Z",
      "clicked": "2023-11-07T05:31:56Z",
      "bounced": "2023-11-07T05:31:56Z",
      "bounce_status": "<string>",
      "unsubscribed": "2023-11-07T05:31:56Z",
      "global_unsubscribed": "2023-11-07T05:31:56Z"
    }
  ]
}

# 
# 
# 
# 
