# /code/list_received_emails.py
# Returns received emails across all active receiving domains, sorted by most recent. Supports cursor-based pagination.
# 
# 
# 
# 
# 
# 
import requests

url = "https://api.paubox.com/v1/email/receiving?limit=25"

headers = {"Authorization": "Bearer <token>"}

response = requests.get(url, headers=headers)

print(response.text)

# HTTP 200: 
# {
#   "object": "list",
#   "data": [
#     {
#       "email_id": "01a0f9e7-9f8e-7303-b771-1bccbe704c4a",
#       "from": [
#         {
#           "address": "sender@example.com",
#           "name": "Jane Doe"
#         }
#       ],
#       "to": [
#         {
#           "address": "sender@example.com",
#           "name": "Jane Doe"
#         }
#       ],
#       "subject": "Patient records request",
#       "received_at": "2026-09-03T14:22:00Z",
#       "has_attachment": false,
#       "size": 3845,
#       "spam": false,
#       "domain": "company.inbound.paubox.email"
#     }
#   ],
#   "has_more": false
# }
# 
# 
# 
