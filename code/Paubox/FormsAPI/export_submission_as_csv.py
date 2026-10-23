# /code/Paubox/FormsAPI/export_submission_as_csv.py
# Paubox Forms API
# Exports a single submission as a CSV attachment. 
# The Content-Disposition filename is derived from the form’s title plus the submission date in Pacific time,
#  e.g. New-Patient-Intake-2026-08-27.csv. 
# Uses the same column layout as the full export (a “Created At” column followed by one column per form field),
#  with a single data row.
# 
# 

import requests

url = "https://api.paubox.com/v1/forms/api/forms/{form_id}/submissions/submission-csv/{submission_id}"

headers = {"Authorization": "Bearer <token>"}

response = requests.get(url, headers=headers)

print(response.text)

# 
# 
# HTTP 200:
# 
# Created At,First name,Last name,Email
# 2024-06-05 02:22:00 PM,Jane,Smith,jane@example.com
# 
# 