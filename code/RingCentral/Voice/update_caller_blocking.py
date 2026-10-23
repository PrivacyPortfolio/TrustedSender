# /code/RingCentral/update_caller_blocking.py
# Block SMS or voice channels entirely

python

import requests

def update_caller_blocking(account_id, extension_id, token, block_settings):
    url = f"https://platform.ringcentral.com/restapi/v1.0/account/{account_id}/extension/{extension_id}/caller-blocking"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.put(url, json=block_settings, headers=headers)
    return response.json()
