"""
Base connection for all tables
"""
from src.config import APP_CONFIG
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class ORMBaseModel():
    def __init__(self):
        #DB CONFIG
        self.db_name = APP_CONFIG.POSTGRES_DB
        self.username = APP_CONFIG.POSTGRES_USER
        self.password = APP_CONFIG.POSTGRES_PASSWORD
        self.host = APP_CONFIG.POSTGRES_HOST

        self.engine = create_engine(f'postgresql://{self.username}:{self.password}@{self.host}:5432/{self.db_name}')
        self.base = declarative_base()
        
        
ORM_CONFIG=ORMBaseModel()