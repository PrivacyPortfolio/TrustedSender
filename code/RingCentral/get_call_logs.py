# code/RingCentral/get_call_logs.py
# Retrieve call logs (detect voice opt out)

python

import requests

def get_call_logs(account_id, extension_id, token):
    url = f"https://platform.ringcentral.com/restapi/v1.0/account/{account_id}/extension/{extension_id}/call-log"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    return response.json()
