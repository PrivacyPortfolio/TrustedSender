# /code/get_tracking_links.py
# Paubox Marketing API
# Return a list of json data for all tracking links associated to a campaign mailing send 
# or campaign mailing delivery.
# Note: The campaign_mailing_send_id is available from the Paubox Marketing interface analytics page. 
# Click a sent campaign and the URL will show a selectedId.
# If you pass in the campaign_mailing_send_id, it will return a list of every link in every email
# sent in the campaign and the tracking info.
# 
# 
# 
import requests

url = "https://api.paubox.com/v1/marketing/tracking_links?order_by=created_at&order=desc"

headers = {"authorization": "<api-key>"}

response = requests.get(url, headers=headers)

print(response.text)

# 
# HTTP 200:
{
  "data": [
    {
      "id": "<string>",
      "type": "tracking_link",
      "attributes": {
        "target_url": "<string>",
        "opened_at": "2023-11-07T05:31:56Z",
        "clicked": 123,
        "campaign_mailing_delivery_id": "<string>"
      }
    }
  ]
}
# 
# 
