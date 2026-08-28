import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "assessments.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AssessmentRecord(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    industry = Column(String)
    overall_risk = Column(String)
    overall_score = Column(Integer)
    request_data = Column(Text)
    response_data = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    Base.metadata.create_all(bind=engine)
