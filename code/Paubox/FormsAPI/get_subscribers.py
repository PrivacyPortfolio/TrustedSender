# /code/get_subscribers.py
# Paubox Marketing API
# Return json data about subscribers
# 
# 
# 
import requests

url = "https://api.paubox.com/v1/marketing/subscribers?items=50&page=1&order_by=created_at&order=desc"

headers = {"authorization": "<api-key>"}

response = requests.get(url, headers=headers)

print(response.text)

# 
# HTTP 200:
# {
  "data": [
    {
      "id": "<string>",
      "type": "subscriber",
      "attributes": {
        "email": "jsmith@example.com",
        "unsubscribed": true,
        "first_name": "<string>",
        "last_name": "<string>"
      }
    }
  ]
}

# HTTP 400:
# {
  "errors": [
    {
      "message": "401 Unauthorized"
    }
  ]
}

# HTTP 401:
# {
  "errors": [
    {
      "message": "401 Unauthorized"
    }
  ]
}

# HTTP 500:
# {
  "errors": [
    {
      "message": "401 Unauthorized"
    }
  ]
}
