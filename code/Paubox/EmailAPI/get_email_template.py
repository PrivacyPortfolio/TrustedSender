# /code/get_email_template.py
# Retrieve a specific dynamic template by ID
# 
# 
# 
# 
import requests

url = "https://api.paubox.com/v1/email/dynamic_templates/{id}"

headers = {"Authorization": "Bearer <token>"}

response = requests.get(url, headers=headers)

print(response.text)

# 
# HTTP 200: 
# {
#   "id": 123,
#   "api_customer_id": 123,
#   "name": "welcome_template",
#   "body": "Hello {{name}}, welcome to our service!",
#   "metadata": {},
#   "created_at": "2023-11-07T05:31:56Z",
#   "updated_at": "2023-11-07T05:31:56Z"
# }
# 
# HTTP 404:
# {
#   "errors": [
#     {
#       "code": 123,
#       "title": "<string>",
#       "details": "<string>"
#     }
#   ]
# }
#  
