import os
from twilio.rest import Client
import asyncio

class TwilioClient:
    def __init__(self):
        self.sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_FROM_NUMBER')
        if self.sid and self.token:
            self.client = Client(self.sid, self.token)
        else:
            self.client = None

    async def send_sms(self, to, body):
        # async wrapper
        return await asyncio.to_thread(self._send_sms_sync, to, body)

    def _send_sms_sync(self, to, body):
        if not self.client:
            print("[twilio] skipping sms (no credentials):", to, body)
            return {"status":"skipped"}
        msg = self.client.messages.create(body=body, from_=self.from_number, to=to)
        return {"sid": msg.sid, "status": msg.status}

    async def send_whatsapp(self, to, body):
        # Twilio WhatsApp uses 'whatsapp:+number'
        return await asyncio.to_thread(self._send_whatsapp_sync, to, body)

    def _send_whatsapp_sync(self, to, body):
        if not self.client:
            print("[twilio] skipping whatsapp (no credentials):", to, body)
            return {"status":"skipped"}
        msg = self.client.messages.create(body=body, from_='whatsapp:'+self.from_number, to='whatsapp:'+to)
        return {"sid": msg.sid, "status": msg.status}
