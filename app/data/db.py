from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from . import models
import os

SQLALCHEMY_DATABASE_URL = (f'{os.getenv("PG_DATABASE_URL", default="postgresql://")}'
                        f'{os.getenv("POSTGRES_USER", default="postgres")}:'
                        f'{os.getenv("POSTGRES_PASSWORD", default="postgres")}@'
                        f'{os.getenv("DB_HOST", default="db-postgres")}:'
                        f'{os.getenv("DB_PORT", default=5432)}/'
                        f'{os.getenv("POSTGRES_DB", default="menu_app")}')


engine = create_engine(SQLALCHEMY_DATABASE_URL)
print(SQLALCHEMY_DATABASE_URL)
if not database_exists(engine.url):
    create_database(engine.url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()