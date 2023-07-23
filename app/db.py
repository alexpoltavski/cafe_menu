from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import os
#from dotenv import load_dotenv, find_dotenv

#load_dotenv(find_dotenv())

#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/menu_app"
SQLALCHEMY_DATABASE_URL = "postgresql://"+os.getenv("DB_USER")+":"+os.getenv("DB_PASSWORD") +"@"+os.getenv("DB_HOST")+":"+os.getenv("DB_PORT")+"/menu_app"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
if not database_exists(engine.url):
    create_database(engine.url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()