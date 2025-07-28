from sqlalchemy import Column, String, DateTime, create_engine, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime
from enum import Enum
from dotenv import load_dotenv
from sqlalchemy.engine.url import make_url
import os

load_dotenv()

DATABASE_URL = os.getenv("DB_URL", "sqlite:///./storage/analysis.db")



url = make_url(DATABASE_URL)
connect_args = {"check_same_thread": False} if url.drivername.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    return SessionLocal()