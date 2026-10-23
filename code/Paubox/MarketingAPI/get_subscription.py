# get_subscription.py
# Paubox Marketing API
# Returns a single subscription by its UUID.
# 
# 
import requests

url = "https://api.paubox.com/v1/marketing/subscriptions/{subscription_id}"

headers = {"authorization": "<api-key>"}

response = requests.get(url, headers=headers)

print(response.text)

# 
# HTTP 200:
{
  "data": {
    "id": 123,
    "uuid": "<string>",
    "subscription_list_id": "<string>",
    "dynamic_list_id": 123,
    "subscriber_id": 123,
    "unsubscribed_at": "2023-11-07T05:31:56Z",
    "delete_at": "2023-11-07T05:31:56Z",
    "created_at": "2023-11-07T05:31:56Z",
    "updated_at": "2023-11-07T05:31:56Z"
  }
}

# 
# 
# 
