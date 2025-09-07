from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# DATABASE CONFIGURATION (sync engine)
# Example: postgresql+psycopg2://username:password@host:port/database?sslmode=require
DATABASE_URL = "postgresql://neondb_owner:npg_SIWRoxsbUw64@ep-empty-silence-ady4qazg-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# CREATE SYNC DATABASE ENGINE
engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

# CREATE SESSION MAKER (sync)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# BASE CLASS FOR DATABASE MODELS
Base = declarative_base()

# DATABASE DEPENDENCY FUNCTION (sync session)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
