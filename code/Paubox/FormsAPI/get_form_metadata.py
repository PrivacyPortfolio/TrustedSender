# /code/Paubox/FormsAPI/get_form_metadata.py
# Paubox Forms API
# Returns the full form definition (HTML, JSON schema, CSS) for a given form. 
# Called by the form embed before rendering a form to a respondent. No authentication required. 
# 
# 
import requests

url = "https://api.paubox.com/v1/forms/public/form_data/{form_id}"

response = requests.get(url)

print(response.text)

# 
# HTTP 200: 
# {
#   "id": "550e8400-e29b-41d4-a716-446655440000",
#   "title": "Patient Intake Form",
#   "description": "Please complete before your appointment.",
#   "form_json": {},
#   "form_html": "<form>...</form>",
#   "form_css": "form { font-family: sans-serif; }",
#   "active": true,
#   "signable": false,
#   "submission_count": 42,
#   "created_at": "2024-01-15T10:30:00Z",
#   "updated_at": "2024-06-01T08:00:00Z"
# }
