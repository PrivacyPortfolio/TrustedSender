# /code/update_email_template.py
# 
# 
# 
# 
import requests

url = "https://api.paubox.com/v1/email/dynamic_templates/{id}"

files = { "data[body]": ("example-file", open("example-file", "rb")) }
payload = { "data[name]": "updated_welcome_template" }
headers = {"Authorization": "Bearer <token>"}

response = requests.patch(url, data=payload, files=files, headers=headers)

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
# HTTP 400:
# {
#   "errors": [
#     {
#       "code": 400,
#       "title": "<string>",
#       "details": "<string>"
#     }
#   ]
# }
# HTTP 404:
# {
#   "errors": [
#     {
#       "code": 404,
#       "title": "<string>",
#       "details": "<string>"
#     }
#   ]
# }
# HTTP 422:
# {
# "errors": [
#     {
#       "code": 422,
#       "title": "Unprocessable Entity",
#       "details": "name: has already been taken"
#     }
#   ]
# }
#  
