# /code/list_email_attachments.py
# Returns attachment metadata for a received email.
# 
# 
import requests

url = "https://api.paubox.com/v1/email/receiving/{email_id}/attachments"

headers = {"Authorization": "Bearer <token>"}

response = requests.get(url, headers=headers)

print(response.text)

# 
# HTTP 200: 
# {
#   "data": [
#     {
#       "id": "56b40f62-bca1-5f96-b547-75e46c4c9f21",
#       "filename": "report.pdf",
#       "content_type": "application/pdf",
#       "size": 12345,
#       "content_id": null,
#       "download_url": "https://api.paubox.com/v1/email/receiving/01a0f9e7-9f8e-7303-b771-1bccbe704c4a/attachments/56b40f62-bca1-5f96-b547-75e46c4c9f21"
#     }
#   ]
# }
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
