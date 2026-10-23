# /code/get_email_disposition.py
# returns 
# HTTP 200:
# {
#   "sourceTrackingId": "6e1cf9a4-7bde-4834-8200-ed424b50c8a7",
#   "data": {
#     "message": {
#       "id": "<f4a9b518-439c-497d-b87f-dfc9cc19194b@authorized_domain.com>",
#       "message_deliveries": [
#         {
#           "recipient": "recipient@host.com",
#           "status": {
#             "deliveryStatus": "delivered",
#             "deliveryTime": "Mon, 23 Apr 2018 13:27:34 -0700",
#             "openedStatus": "opened",
#             "openedTime": "Mon, 23 Apr 2018 13:27:51 -0700"
#           }
#         }
#       ],
#       "total_opens": 1,
#       "distinct_opens": 1,
#       "total_click_count": 2,
#       "clicks_per_link": [
#         {
#           "click_count": 1,
#           "target_url": "amazon.com"
#         },
#         {
#           "click_count": 1,
#           "target_url": "ebay.com"
#         }
#       ],
#       "unsubscribed": false
#     }
#   }
# }
# HTTP 404:
# {
#   "errors": [
#     {
#       "code": 404,
#       "title": "Not Found",
#       "details": "message not found"
#     }
#   ]
# }
# 
curl --request GET \
  --url https://api.paubox.com/v1/email/message_receipt \
  --header 'Authorization: Bearer <token>'