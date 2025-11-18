# Minimal DB layer using SQLAlchemy. Encrypted logs using Fernet symmetric encryption.
from sqlalchemy import create_engine, Column, Integer, Text, LargeBinary, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os, json, datetime
from cryptography.fernet import Fernet

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
FERNET_KEY = os.getenv("FERNET_KEY")
if not FERNET_KEY:
    # NOT FOR PRODUCTION: create ephemeral key if not provided
    FERNET_KEY = Fernet.generate_key().decode()
fernet = Fernet(FERNET_KEY.encode())

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class EncryptedLog(Base):
    __tablename__ = "encrypted_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(128), index=True)
    payload = Column(LargeBinary)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    @staticmethod
    def create(db, user_id, payload, meta=None):
        record = EncryptedLog(user_id=user_id, payload=fernet.encrypt(json.dumps({"payload":payload,"meta":meta}).encode()))
        db.add(record); db.commit(); db.refresh(record)
        return record

def get_db():
    return SessionLocal()

def init_db():
    Base.metadata.create_all(bind=engine)
    return True
