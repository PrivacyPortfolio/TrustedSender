# /code/get_subscribers_by_tracking_link.py
# Paubox Marketing API
# Returns json data about subscribers for a specific tracking link
# 
# 
import requests

url = "https://api.paubox.com/v1/marketing/analytics/subscribers_by_tracking_link"

headers = {"authorization": "<api-key>"}

response = requests.get(url, headers=headers)

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
        "custom_fields": [
          {
            "subscriber_custom_field_type_id": "<string>",
            "name": "<string>",
            "value": "<string>"
          }
        ]
      }
    }
  ]
}

# 
# 
# 
# 
