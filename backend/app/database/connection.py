from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://neondb_owner:npg_MVJPsg6a4RCW@ep-patient-voice-abdqvq2n-pooler.eu-west-2.aws.neon.tech/taller_mecanic?sslmode=require&channel_binding=require"

engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()