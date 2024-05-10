"""
ORM for Table 'Buildings'
"""

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
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

    # Define the relationship with the FloorsModel table
    floors = relationship("FloorsModel", back_populates="building")

    # Create tables in the database
    base.metadata.create_all(engine, checkfirst=True)


class BuildingUtils:
    def create_building_record(self, request_data):
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            # Create a new Building object
            new_building = BuildingsModel(
                building_id=str(uuid.uuid4()),
                name=request_data['name'],
                description=request_data['description'],
                owner_history=request_data['owner_history'],
                address_lines=request_data['address_lines'],
                postal_box=request_data.get('postal_box'),
                town=request_data['town'],
                region=request_data['region'],
                postal_code=request_data.get('postal_code'),
                country=request_data['country']
            )
            # Add the new_building object to the session
            session.add(new_building)
            # Commit the transaction to the database
            session.commit()
            # Close the session
            session.close()
            print({"message": "Building added successfully", "building": new_building})
            return True, 201
        except IntegrityError:
            session.rollback()
            print({"error": "An error occurred while adding the building"})
            return False, 500

    def get_all_buildings(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        # Query all buildings
        buildings = session.query(BuildingsModel).all()
        # Close the session
        session.close()
        return buildings

    def delete_bulding_by_id(self, building_id):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            # Query WindowsCoordinatesModel to get coordinates related to the window_id
            buildings_query = session.query(BuildingsModel).filter_by(building_id=building_id)
            # Delete coordinates related to the window_id
            buildings_query.delete()

            # Commit the transaction
            session.commit()
            print("Record deleted successfully.")
            return True, 200
        except IntegrityError:
            session.rollback()
            print("An error occurred while delete window records")
            return False, 500
        finally:
            session.close()