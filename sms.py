import json

from twilio.rest import Client

CONFIG = None
with open('/Users/janarth.punniyamoorthyopendoor.com/personal-git/manga-downloader/configs/twilio.json', 'r') as f:
    CONFIG = json.load(f)

def get_twilio_client():
    return Client(
        username=CONFIG['account_sid'],
        password=CONFIG['auth_token'],
    )

# https://www.twilio.com/docs/messaging/services/tutorials/send-messages-with-messaging-services#maincontent
def send_sms(
    message_body='',
    recipient_phone_num=''
):
    twilio_client = get_twilio_client()
    kwargs = {
        'body': message_body,
        'messaging_service_sid': CONFIG['messaging_service_sid'],
        'to': recipient_phone_num,
    }

    response = twilio_client.messages.create(**kwargs)
    return response
