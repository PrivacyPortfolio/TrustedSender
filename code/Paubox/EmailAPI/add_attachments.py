# /code/Paubox/EmailAPI/add_attachments.py
# REST API for attach files to emails sent with the Paubox Email API
# (see https://docs.paubox.com/email-api/attachments for attachment fields and Base64 content.)
# Usage limitation: The whole request body, including Base64-encoded attachments, must not exceed 50 MB. 
#   Base64 adds about a third to file size, so plan for roughly 37 MB of raw files per message.
#
{
  "data": {
    "message": {
      "recipients": ["recipient@host.com"],
      "headers": {
        "subject": "Sample email with an attachment",
        "from": "sender@verifieddomain.com"
      },
      "content": {
        "text/plain": "Hello World!"
      },
      "attachments": [
        {
          "fileName": "hello_world.txt",
          "contentType": "text/plain",
          "content": "SGVsbG8gV29ybGQh"
        }
      ]
    }
  }
}
