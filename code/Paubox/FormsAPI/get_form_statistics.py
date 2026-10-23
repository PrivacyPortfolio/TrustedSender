# /code/Paubox/FormsAPI/get_form_statistics.py
# Paubox Forms API
# Returns aggregate form statistics for a customer: 
# the number of active forms, the total submission count, and the number of submissions received in the last 7 days.
# 
# 

import requests

url = "https://api.paubox.com/v1/forms/api/forms/stats"

headers = {"Authorization": "Bearer <token>"}

response = requests.get(url, headers=headers)

print(response.text)

# 
# 
# HTTP 200:
# {
#   "active_form_count": 8,
#   "total_submission_count": 1204,
#   "submissions_last_7_days": 37
# }
# 
# 