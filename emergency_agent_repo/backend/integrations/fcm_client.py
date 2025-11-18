import os, json
import firebase_admin
from firebase_admin import messaging, credentials

_initialized = False

class FCMClient:
    def __init__(self):
        global _initialized
        sa_path = os.getenv("FCM_SERVICE_ACCOUNT_JSON_PATH")
        if sa_path and not _initialized:
            cred = credentials.Certificate(sa_path)
            firebase_admin.initialize_app(cred)
            _initialized = True

    async def send_push(self, contacts, title, body):
        # contacts is list of dicts with device token under 'device_token' (demo)
        tokens = [c.get("device_token") for c in contacts if c.get("device_token")]
        if not tokens:
            print("[fcm] no tokens to send")
            return {"status":"skipped"}
        message = messaging.MulticastMessage(
            notification=messaging.Notification(title=title, body=body),
            tokens=tokens
        )
        response = messaging.send_multicast(message)
        return {"success_count": response.success_count, "failure_count": response.failure_count}
