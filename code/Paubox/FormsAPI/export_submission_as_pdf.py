# /code/Paubox/FormsAPI/export_submission_as_pdf.py
# Paubox Forms API
# Exports a single submission as a PDF attachment. 
# The Content-Disposition filename is derived from the form’s title plus the submission date in Pacific time, 
# e.g. New-Patient-Intake-2026-08-27.pdf; titles are reduced to alphanumerics, - and _. 
# For signable forms, the PDF includes the respondent’s signature images.
# 
# 

import requests

url = "https://api.paubox.com/v1/forms/api/forms/{form_id}/submissions/{submission_id}/submission-pdf"

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