# /code/Paubox/FormsAPI/submit_form_response.py
# Paubox Forms API
# Submits a respondent’s answers for a form. No authentication required. 
# On success, the service stores the submission, increments the form’s submission count, 
# emails recipients (if configured), and returns 201 with no body.
# Maximum request size is 250 MB (to support file attachments).
# 
# 

import requests

url = "https://api.paubox.com/v1/forms/api/forms/{form_id}/submissions"

payload = {
    "form_data": {
        "first_name": "Jane",
        "signature": "{signature_field}"
    },
    "attachments": [
        {
            "name": "consent.pdf",
            "content": "JVBERi0xLjQ..."
        }
    ]
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)

print(response.text)

# 
# 
# 