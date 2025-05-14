import requests
import os
from twilio.rest import Client


ACCOUNT_SID = os.getenv("TWILIO_ACOUNT_ID")
ACCOUNT_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER_FROM = os.getenv("TWILIO_NUMBER_FROM")
TWILIO_NUMBER_TO = os.getenv("TWILIO_NUMBER_TO")


class TwilioService:
    def __init__(
        self,
        account_sid=ACCOUNT_SID,
        auth_token=ACCOUNT_AUTH_TOKEN,
        from_whatsapp_number=TWILIO_NUMBER_FROM,
        to_whatsapp_number=TWILIO_NUMBER_TO
    ):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_whatsapp_number = from_whatsapp_number
        self.to_whatsapp_number = to_whatsapp_number
        self.client = Client(self.account_sid, self.auth_token)

    def send_message(self, body):
        message = self.client.messages.create(
            body=body,
            from_=self.from_whatsapp_number,
            to=self.to_whatsapp_number
        )
        print(message.sid)
