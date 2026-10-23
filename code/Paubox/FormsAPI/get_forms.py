# /code/Paubox/FormsAPI/get_forms.py
# Paubox Forms API
# Returns a paginated list of forms belonging to a customer. 
# Supports filtering by form ID, title/description search, and archived/active state, plus ordering and pagination.
# 
# 

import requests

url = "https://api.paubox.com/v1/forms/api/forms?order_by=created_at&order=desc&page=1&items=50"

headers = {"Authorization": "Bearer <token>"}

response = requests.get(url, headers=headers)

print(response.text)

# 
# HTTP 200:
# {
#   "results": [
#     {
#       "id": "550e8400-e29b-41d4-a716-446655440000",
#       "title": "Patient Intake Form",
#       "description": "Please complete before your appointment.",
#       "form_html": "<form>...</form>",
#       "form_json": {},
#       "form_css": "form { font-family: sans-serif; }",
#       "vanity_url": null,
#       "version": 2,
#       "active": true,
#       "customer_id": 123,
#       "old_form_id": null,
#       "recipient": "intake@example.com,records@example.com",
#       "signable": false,
#       "signature_confirmation_label": null,
#       "submission_count": 42,
#       "type": null,
#       "subscription_list_id": null,
#       "deleted": false,
#       "archived": false,
#       "created_at": "2024-01-15T10:30:00Z",
#       "updated_at": "2024-06-01T08:00:00Z"
#     }
#   ],
#   "page_info": {
#     "count": 1,
#     "pages": 1,
#     "page": 1,
#     "items": 50
#   }
# }
# 
# 
# 