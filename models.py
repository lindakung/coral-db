from sqlalchemy import create_engine, Column, String, Integer 
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings

DeclarativeBase = declarative_base()

def db_connect():
    """
    Performs database connection using db settings from settings.py
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))

def create_corals_table(engine):

    DeclarativeBase.metadata.create_all(engine)

class Corals(DeclarativeBase):
    
    __tablename__ = "corals"

    id = Column(Integer, primary_key=True)
    full_genus = Column('full_genus', String)
    name = Column('name', String)
    genus = Column('genus', String)
    coral_type = Column('coral_type', String)
    color = Column('color', ARRAY(String), nullable=True)
    feeding = Column('feeding', String, nullable=True)
    flow = Column('flow', String, nullable=True)
    lighting = Column('lighting', String, nullable=True)
    image = Column('image', String, nullable=True)

