# /code/create_subscriber.py
# Paubox Marketing API
# Creates a subscriber record. 
# Adds record to subscription list if specified otherwise adds to all contacts.
# 
# 
import requests

url = "https://api.paubox.com/v1/marketing/subscribers"

payload = { "subscriber": {
        "email": "test@example.com",
        "first_name": "test",
        "last_name": "example"
    } }
headers = {
    "authorization": "<api-key>",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)

# 
# HTTP 200: 
# {
#   "data": {
#     "id": "<string>",
#     "type": "subscriber",
#     "attributes": {
#       "email": "jsmith@example.com",
#       "unsubscribed": true,
#       "first_name": "<string>",
#       "last_name": "<string>"
#     }
#   }
# }

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

# HTTP 422: 
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

# 