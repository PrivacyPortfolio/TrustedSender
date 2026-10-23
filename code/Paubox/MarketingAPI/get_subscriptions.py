# /code/get_subscriptions.py
# Paubox Marketing API
# Returns every subscription belonging to the authenticated customer. 
# A subscription is the join between a subscriber and a subscription list (or a dynamic list),
# and it carries the unsubscribed_at timestamp that marks a list-level opt-out.
# This endpoint is not paginated and returns raw subscription records.
# 
# 
import requests

url = "https://api.paubox.com/v1/marketing/subscriptions"

headers = {"authorization": "<api-key>"}

response = requests.get(url, headers=headers)

print(response.text)

# 
# HTTP 200:
# {
  "data": [
    {
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
  ]
}

# HTTP 200:
# 
# HTTP 200:
# 
# 
