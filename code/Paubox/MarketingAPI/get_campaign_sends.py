# get_campaign_sends.py
# Paubox Marketing API
# Return json data information about campaigns sent
# 
# 
# 
import requests

url = "https://api.paubox.com/v1/marketing/analytics/campaign_mailing_sends_table?order_by=sent_at&order=desc"

headers = {"authorization": "<api-key>"}

response = requests.get(url, headers=headers)

print(response.text)

# 
# HTTP 200:
{
  "data": [
    {
      "id": "<string>",
      "marketing_email_id": "<string>",
      "campaign_mailing_id": "<string>",
      "campaign_mailing_created_at": "2023-11-07T05:31:56Z",
      "sent_at": "2023-11-07T05:31:56Z",
      "subscription_list_name": "<string>"
    }
  ]
}

# 
# 
