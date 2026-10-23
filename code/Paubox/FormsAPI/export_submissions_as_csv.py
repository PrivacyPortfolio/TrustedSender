# /code/Paubox/FormsAPI/export_submissions_as_csv.py
# Paubox Forms API
# Exports all submissions of a form as a CSV attachment. 
# The Content-Disposition filename is derived from the form’s title 
# plus the export date in Pacific time, 
# e.g. New-Patient-Intake-submissions-2026-08-27.csv. 
# The first column is “Created At”, followed by one column per form field, 
# using the field labels from the form definition.
# 
# 

import requests

url = "https://api.paubox.com/v1/forms/api/forms/{form_id}/submissions/submission-csv"

headers = {"Authorization": "Bearer <token>"}

response = requests.get(url, headers=headers)

print(response.text)

# 
# 
# HTTP 200:
# 
# Created At,First name,Last name,Email
# 2024-06-05 02:22:00 PM,Jane,Smith,jane@example.com
# 2024-06-04 09:10:00 AM,John,Doe,john@example.com
# 
# 