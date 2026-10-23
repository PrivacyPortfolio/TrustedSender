# /code/get_received_email.py
# Returns the full content of a single received email, including headers, body, and attachment metadata.
# 
# 
# 
# 
# 

import requests

url = "https://api.paubox.com/v1/email/receiving/{email_id}"

headers = {"Authorization": "Bearer <token>"}

response = requests.get(url, headers=headers)

print(response.text)

# 
# HTTP 200: 
# {
#   "data": {
#     "email_id": "01a0f9e7-9f8e-7303-b771-1bccbe704c4a",
#     "from": [
#       {
#         "address": "sender@example.com",
#         "name": "Jane Doe"
#       }
#     ],
#     "to": [
#       {
#         "address": "sender@example.com",
#         "name": "Jane Doe"
#       }
#     ],
#     "cc": [
#       {
#         "address": "sender@example.com",
#         "name": "Jane Doe"
#       }
#     ],
#     "subject": "<string>",
#     "date": "<string>",
#     "received_at": "2023-11-07T05:31:56Z",
#     "message_id": [
#       "<string>"
#     ],
#     "in_reply_to": [
#       "<string>"
#     ],
#     "references": [
#       "<string>"
#     ],
#     "text_body": "<string>",
#     "html_body": "<string>",
#     "size": 123,
#     "spam": true,
#     "spam_score": 123,
#     "authentication": {
#       "spf": "pass",
#       "dkim": "pass",
#       "dmarc": "pass"
#     },
#     "domain": "<string>",
#     "headers": [
#       {
#         "name": "<string>",
#         "value": "<string>"
#       }
#     ],
#     "attachments": [
#       {
#         "id": "56b40f62-bca1-5f96-b547-75e46c4c9f21",
#         "filename": "<string>",
#         "content_type": "<string>",
#         "size": 123,# 
#         "content_id": "<string>",
#         "download_url": "https://api.paubox.com/v1/email/receiving/01a0f9e7-9f8e-7303-b771-1bccbe704c4a/attachments/56b40f62-bca1-5f96-b547-75e46c4c9f21"
#       }
#     ]
#   }
# }
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
# 
# 
