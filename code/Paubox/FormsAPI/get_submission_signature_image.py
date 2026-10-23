# /code/Paubox/FormsAPI/get_submission_signature_image.py
# Paubox Forms API
# Returns the signature image captured for a signature field on a submission, as a PNG. 
# The response is sent with Cache-Control: no-store, private.
# 
# 

import requests

url = "https://api.paubox.com/v1/forms/api/forms/{form_id}/submissions/{submission_id}/signature/{field_name}"

headers = {"Authorization": "Bearer <token>"}

response = requests.get(url, headers=headers)

print(response.text)

# 
# 
# HTTP 200:
# 
# "<string>"
# 
# 