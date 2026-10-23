# /code/RingCentral/delete_call_log.py
# Delete call logs (privacy enforcement)

python

import requests

def delete_call_log(account_id, extension_id, call_record_id, token):
    url = f"https://platform.ringcentral.com/restapi/v1.0/account/{account_id}/extension/{extension_id}/call-log/{call_record_id}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.delete(url, headers=headers)
    return response.json()
