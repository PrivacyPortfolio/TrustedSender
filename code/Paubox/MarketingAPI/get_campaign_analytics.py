# /code/get_campaign_analytics.py
# Paubox Marketing API
# Return json data statistics about campaigns sent
# 
# 
# 
import requests

url = "https://api.paubox.com/v1/marketing/analytics/campaign_mailing_send_totals"

headers = {"authorization": "<api-key>"}

response = requests.get(url, headers=headers)

print(response.text)

# 
# HTTP 200:
{
  "data": {
    "delivered": 123,
    "viewed": 123,
    "clicked": 123,
    "bounced": 123,
    "soft_bounced": 123,
    "hard_bounced": 123,
    "unsubscribed": 123,
    "global_unsubscribed": 123
  }
}

# 
# 
