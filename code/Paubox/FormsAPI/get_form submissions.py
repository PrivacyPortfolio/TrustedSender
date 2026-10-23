# /code/Paubox/FormsAPI/get_form submissions.py
# Paubox Forms API
# Returns a paginated list of submissions for a form. 
# Each submission’s form_data field is a JSON-encoded string of the respondent’s answers.
# 
# 

import requests

url = "https://api.paubox.com/v1/forms/api/forms/{form_id}/submissions?order_by=created_at&order=desc&page=1&items=50"

headers = {"Authorization": "Bearer <token>"}

response = requests.get(url, headers=headers)

print(response.text)

# 
# 
# HTTP 200:
# {
#   "data": [
#     {
#       "id": "1a2b3c4d-5e6f-4a7b-8c9d-0e1f2a3b4c5d",
#       "form_id": "550e8400-e29b-41d4-a716-446655440000",
#       "form_data": "{\"first_name\":\"Jane\",\"last_name\":\"Smith\",\"email\":\"jane@example.com\"}",
#       "storage_type": "S3",
#       "storage_url": null,
#       "submitter_email": "jane@example.com",
#       "recipients": "intake@example.com",
#       "attachment_name": null,
#       "attachment_url": null,
#       "attachment_type": null,
#       "attachment": null,
#       "created_at": "2024-06-05T14:22:00Z"
#     }
#   ],
#   "total": 42,
#   "page": 1,
#   "items": 50
# }
# 
# 