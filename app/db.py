import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

db_engine = create_engine(os.getenv("DB_URL"))
SessionLocal = sessionmaker(bind=db_engine)

Base = declarative_base()