# /code/send_templated_email.py
# Send an email using a dynamic template with variable substitution
# 
# 
# 
import requests

url = "https://api.paubox.com/v1/email/templated_messages"

payload = {
     "data": {
        "template_name": "ChangeOfAddress",
        "template_values": {
          "CP_domain": "example.com",
          "CP_org_name": "Example Org",
          "M_message_uuid": "123e4567-e89b-12d3-a456-426614174000",
          "M_message_type": "change_of_address",
          "CTP_sender_id": "sender-001",
          "trusted_sender_tag": "trusted",
          "CP_sender_prior_email_display_name": "Craig",
          "CP_sender_prior_email": "craig@oldmail.com",
          "CP_sender_email": "craig@newmail.com",
          "CP_location": "Alameda, CA",
          "M_sent_date": "2026-10-20",
          "CTP_contact_email": "recipient@example.com",
          "CTP_org_name": "Recipient Org",
          "CP_sender_email_display_name": "Craig Newmail",
          "CP_sender_telephone": "555-123-4567",
          "CP_sender_telephone_display_name": "Craig Mobile",
          "CP_contact_email_display_name": "Support Team",
          "CP_contact_email": "support@example.com",
          "CP_contact_telephone": "555-987-6543",
          "CP_contact_telephone_display_name": "Support Line"

payload = {
    "data": {
        "template_name": "ChangeOfAddress",
        "template_values": template_values,
        "message": {
            "recipients": ["recipient@host.com", "Recipient Name <recipient2@host.com>"],
            "bcc": ["recipient3@host.com", "Recipient Name <recipient4@host.com>"],
            "headers": {
                "subject": "Change of Address Notification",
                "from": "sender@authorized_domain.com",
                "reply-to": "Sender Name <sender@authorized_domain.com>",

                "X-Message-UUID": template_values["M_message_uuid"],
                "X-Vendor-ID": template_values["vendor_id"],
                "X-Trusted-Sender-Tag": template_values["trusted_sender_tag"],
                "X-Origin-Domain": template_values["CP_domain"],
                "X-Sender-System": "PrivacyPortfolio"
            }
        }
    }
}
            "allowNonTLS": False,
            "forceSecureNotification": False,
            "attachments": [
                {
                    "fileName": "hello_world.txt",
                    "contentType": "text/plain",
                    "content": "SGVsbG8gV29ybGQ"
                }
            ]
        }
    } }
headers = {
    "Authorization": "Bearer <token>",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)

# HTTP 200:
# {
#   "sourceTrackingId": "3d38ab13-0af8-4028-bd45-XXXXXXXXXXXX",
#   "data": "Service OK"
# }

# HTTP 400
# {
#   "errors": [
#     {
#       "code": 400,
#       "title": "Template values missing",
#       "details": "Request is missing a template_values parameter"
#     }
#   ]
# }

# HTTP 401:
# {
#   "errors": [
#     {
#       "code": 401,
#       "title": "Invalid Access Token",
#       "details": "Access token is missing or does not match endpoint username"
#     }
#   ]
# }

# HTTP 403:
# {
#   "errors": [
#     {
#       "code": 403,
#       "title": "Account Under Review",
#       "details": "New accounts are under review for 24 hours after signup. Please try again later or contact support."
#     }
#   ]
# }

# HTTP 404:
# {
#   "errors": [
#     {
#       "code": 404,
#       "title": "Template not found",
#       "details": "No dynamic template with the given name exists for this account"
#     }
#   ]
# }

# HTTP 422:
# {
#   "errors": [
#     {
#       "code": 422,
#       "title": "Template compilation failed",
#       "details": "The dynamic template could not be rendered with the provided values"
#     }
#   ]
# }

