# /code/list_receiving_domains.py
# Returns all receiving domains for the authenticated account.
# 
import requests

url = "https://api.paubox.com/v1/email/receiving/domains"

headers = {"Authorization": "Bearer <token>"}

response = requests.get(url, headers=headers)

print(response.text)

# HTTP 200:
# {
#   "data": [
#     {
#       "id": 1,
#       "domain": "support.inbound.paubox.email",
#       "customer_id": 1001,
#       "state": "active",
#       "mx_verified": true,
#       "dkim_public_key": "<string>",
#       "dns_zone_file": "<string>",
#       "created_at": "2023-11-07T05:31:56Z",
#       "updated_at": "2023-11-07T05:31:56Z"
#     }
#   ]
# }
