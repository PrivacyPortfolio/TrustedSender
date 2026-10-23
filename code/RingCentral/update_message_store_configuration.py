# /code/RingCentral/update_message_store_configuration.py
# Limit RingCentral processing (Intermediary Party limits)

python

import requests

def update_message_store_configuration(account_id, extension_id, token, config):
    url = f"https://platform.ringcentral.com/restapi/v1.0/account/{account_id}/extension/{extension_id}/message-store-configuration"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.put(url, json=config, headers=headers)
    return response.json()
