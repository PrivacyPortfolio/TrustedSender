# /code/get_subscriber.py
# Paubox Marketing API
# Return json data about subscriber. 
# If no subscriber matches subscriber_id, the response is 200 with {"data": null}.
# 
import requests

url = "https://api.paubox.com/v1/marketing/subscribers/{subscriber_id}"

headers = {"authorization": "<api-key>"}

response = requests.get(url, headers=headers)

print(response.text)

# 
# HTTP 200:
{
  "data": {
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
}
