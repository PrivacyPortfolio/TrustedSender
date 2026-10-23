# /code/Paubox/EmailAPI/send_email_message.py
# Paubox Email API
# Send a single HIPAA compliant email with the Paubox Email API. 
# Supports cc, bcc, custom headers, attachments, and open and link tracking overrides.
# Returns a sourceTrackingId which can used to check delivery status later.
#   

import requests

url = "https://api.paubox.com/v1/email/messages"

payload = { "data": {
        "message": {
            "recipients": ["recipient@host.com", "Recipient Name <recipient2@host.com>"],
            "bcc": ["recipient3@host.com", "Recipient Name <recipient4@host.com>"],
            "cc": ["cc.name <cc@example.com>"],
            "headers": {
                "subject": "sample email",
                "from": "sender@authorized_domain.com",
                "reply-to": "Sender Name <sender@authorized_domain.com>",
                "x-custom-header": "sample custom header",
                "List-Unsubscribe": "<mailto:unsubscribe@yourdomain.com?subject=unsubscribe>"
            },
            "content": {
                "text/plain": "Hello World!",
                "text/html": "<html><body><h1>Hello World!</h1></body></html>"
            },
            "attachments": [
                {
                    "fileName": "hello_world.txt",
                    "contentType": "text/plain",
                    "content": "SGVsbG8gV29ybGQh"
                }
            ]
        },
        "override_open_tracking": True,
        "override_link_tracking": True,
        "unsubscribe_url": "https://your_url_here.com"
    } }
headers = {
    "Authorization": "Bearer <token>",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)


# HTTP 200:
# 
# {
#   "sourceTrackingId": "3d38ab13-0af8-4028-bd45-52e882e0d584",
#   "customHeaders": {
#     "X-Custom-Header": "value"
#   },
#   "data": "Service OK"
# }

