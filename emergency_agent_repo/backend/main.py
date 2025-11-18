from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import os, asyncio, json, datetime
from integrations.twilio_client import TwilioClient
from integrations.fcm_client import FCMClient
from integrations.osm_utils import find_nearest_responder
from vertex.intent import classify_intent
from db import get_db, EncryptedLog, init_db
from tasks.escalation import schedule_escalation

app = FastAPI(title="Multimodal Emergency Agent")

# init DB at startup
@app.on_event("startup")
async def startup():
    await init_db()

class EmergencyIn(BaseModel):
    user_id: str
    text: str = None
    lat: float = None
    lon: float = None
    voice_transcript: str = None
    contacts: list = []

@app.post("/api/emergency")
async def emergency(payload: EmergencyIn, request: Request):
    # 1) classify intent
    intent = await classify_intent(payload.text or payload.voice_transcript or "")
    # 2) determine location (fallback if missing)
    lat = payload.lat or 0.0
    lon = payload.lon or 0.0
    # 3) find nearest responder (OSM / placeholder for 108)
    responder = await find_nearest_responder(lat, lon, responder_type="ambulance")
    # 4) dispatch via Twilio + FCM
    tw = TwilioClient()
    fcm = FCMClient()
    message = f"EMERGENCY: {intent.get('label','unknown')} — location: {lat},{lon}"
    # send SMS/WhatsApp to responder and contacts
    contacts = payload.contacts[:3]
    notify_tasks = []
    for c in contacts:
        notify_tasks.append(tw.send_sms(c.get('phone'), message))
    # send to central responder / 108 (placeholder)
    if responder and responder.get("phone"):
        notify_tasks.append(tw.send_whatsapp(responder["phone"], message))
    # send push
    notify_tasks.append(fcm.send_push(contacts, title="Emergency Alert", body=message))
    results = await asyncio.gather(*notify_tasks, return_exceptions=True)
    # 5) log encrypted
    db = get_db()
    log = EncryptedLog.create(db, user_id=payload.user_id, payload=dict(payload), meta={"intent": intent, "responder": responder})
    # 6) schedule escalation
    await schedule_escalation(log.id, delay_seconds=120)  # escalate after 2 minutes if not resolved
    return {"status": "dispatched", "intent": intent, "responder": responder}

@app.get("/health")
def health():
    return {"status":"ok", "time": datetime.datetime.utcnow().isoformat()}
