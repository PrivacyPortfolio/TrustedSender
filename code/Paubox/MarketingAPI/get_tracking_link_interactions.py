# /code/get_tracking_link_interactions.py
# Paubox Marketing API
# Returns json data about interactions with tracking links
# 
# 
# 

import requests

url = "https://api.paubox.com/v1/marketing/analytics/tracking_links_by_unique_link?order_by=clicked&order=desc"

headers = {"authorization": "<api-key>"}

response = requests.get(url, headers=headers)

print(response.text)


# 
# HTTP 200:
# {
  "data": [
    {
      "html_id": 123,
      "target_url": "<string>",
      "clicked": 123
    }
  ]
}

# 