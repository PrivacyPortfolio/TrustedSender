# /code/RingCentral/delete_sms_message.py
# Delete SMS for suppression or privacy enforcement

python

import requests

def delete_sms_message(account_id, extension_id, message_id, token):
    url = f"https://platform.ringcentral.com/restapi/v1.0/account/{account_id}/extension/{extension_id}/message-store/{message_id}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.delete(url, headers=headers)
    return response.json()
