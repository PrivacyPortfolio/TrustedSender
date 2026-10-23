# /code/download_attachment.py
# Downloads a received email attachment as raw bytes.
# 
# 
# 
import requests

url = "https://api.paubox.com/v1/email/receiving/{email_id}/attachments/{attachment_id}"

headers = {"Authorization": "Bearer <token>"}

response = requests.get(url, headers=headers)

print(response.text)

# 
# HTTP 200:
# "<string>"
# 
# HTTP 404:
# {
#   "errors": [
#     {
#       "code": 123,
#       "title": "<string>",
#       "details": "<string>"
#     }
#   ]
# }
# 
