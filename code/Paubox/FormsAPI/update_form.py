# /code/Paubox/FormsAPI/update_form.py
# Paubox Forms API
# Updates a form. This is a partial update: any fields omitted from the request body are left unchanged.
# 
# 

import requests

url = "https://api.paubox.com/v1/forms/api/forms/{form_id}"

payload = {
    "title": "Patient Intake Form (2024)",
    "active": True
}
headers = {
    "Authorization": "Bearer <token>",
    "Content-Type": "application/json"
}

response = requests.put(url, json=payload, headers=headers)

print(response.text)

# 
# HTTP 200:
# {
#   "detail": "Form updated successfully",
#   "form_id": "550e8400-e29b-41d4-a716-446655440000"
# }

# 
# HTTP 422:
# {
#   "message": "form_json.body[1].type `DatePicker` is not a component the form renderer knows; expected one of: Text, Divider, TextInput, TextArea, Dropdown, Checkboxes, Radiobutton, FileUpload, Signature, Button, Conditional, Logo"
# }
# 
# 

