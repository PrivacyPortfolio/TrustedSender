# /code/get_subscription_lists.py
# Paubox Marketing API
# Return json data about subscription lists
# 
# 
# 
import requests

url = "https://api.paubox.com/v1/marketing/subscription_lists"

headers = {"authorization": "<api-key>"}

response = requests.get(url, headers=headers)

print(response.text)

# 
# HTTP 200:
{
  "data": [
    {
      "id": "<string>",
      "type": "subscription_list",
      "attributes": {
        "name": "<string>",
        "is_default": true,
        "subscriber_count": 123,
        "form_id": "<string>"
      }
    }
  ]
}

# 
# 
