"""
ORM for Table 'Buildings'
"""

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
from src.models import ORM_CONFIG

# Define SQLAlchemy engine
engine = ORM_CONFIG.engine

# Define base class for declarative mapping
base = ORM_CONFIG.base

# Define Building class to represent the Building table
class BuildingsModel(base):
    __tablename__ = 'buildings'

    building_id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    name = Column(String(50))
    description = Column(String(50))
    owner_history = Column(String(20))
    address_lines = Column(String(50))
    postal_box = Column(Integer)
    town = Column(String(20))
    region = Column(String(20))
    postal_code = Column(Integer)
    country = Column(String(20))

    # Create tables in the database
    base.metadata.create_all(engine, checkfirst=True)

class BuildingUtils:
    def create_building_record(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        # Create a new Building object
        new_building = BuildingsModel(
            name='Burj Khalifa',
            description='tallest sky scraper in the world',
            owner_history='Test User Name',
            address_lines='Main City, Dubai',
            postal_box=123,
            town='Dubai',
            region='Middle-East',
            postal_code=12345,
            country='UAE'
        )
        # Add the new_building object to the session
        session.add(new_building)
        # Commit the transaction to the database
        session.commit()
        # Close the session
        session.close()
    
    def get_all_buildings(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        # Query all buildings
        buildings = session.query(BuildingsModel).all()
        # Close the session
        session.close()
        return buildings
