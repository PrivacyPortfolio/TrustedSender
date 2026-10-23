# /code/unsubscribe_subscribers.py
# Paubox Marketing API
# Unsubscribes one or more subscribers, identified by their UUIDs.
# When subscription_list_ids is supplied, 
# the matching subscriptions are stamped with unsubscribed_at 
# and the subscribers remain subscribed to every other list. 
# When it is omitted, the subscribers are globally opted out by stamping opted_out_on, 
# which suppresses all future marketing email to them.
# 
# 
import requests

url = "https://api.paubox.com/v1/marketing/subscriptions/unsubscribe"

payload = {
    "subscriber_ids": ["8f14e45f-ceea-467a-9f2c-4b3d2a1e5c60"],
    "subscription_list_ids": ["123e4567-e89b-12d3-a456-426614174000"]
}
headers = {
    "authorization": "<api-key>",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)

# 
# HTTP 200:
{
  "data": [
    {
      "id": "<string>",
      "type": "<string>",
      "attributes": {
        "email": "jsmith@example.com",
        "first_name": "<string>",
        "last_name": "<string>",
        "unsubscribed": true,
        "created_at": "2023-11-07T05:31:56Z",
        "updated_at": "2023-11-07T05:31:56Z",
        "custom_fields": [
          {
            "subscriber_custom_field_type_id": "<string>",
            "name": "<string>",
            "value": "<string>"
          }
        ],
        "subscription_lists": [
          {
            "id": "<string>",
            "name": "<string>",
            "unsubscribed": true
          }
        ],
        "statistics": {
          "deliveries": 123,
          "delivered": 123,
          "opened": 123,
          "clicked": 123,
          "soft_bounced": 123,
          "hard_bounced": 123,
          "unsubscribed": 123,
          "global_unsubscribed": 123
        }
      }
    }
  ],
  "errors": "<string>"
}

# 
# 
