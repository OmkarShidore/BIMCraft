from sqlalchemy.orm import relationship
from sqlalchemy import Column, ARRAY, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, DataError
from src.models import ORM_CONFIG
import uuid
from sqlalchemy.dialects.postgresql import UUID, ARRAY, FLOAT
from src.common.utils import get_3d_rotation_matrix, rotate_3d_coordinates

# Define SQLAlchemy engine
engine = ORM_CONFIG.engine

# Define base class for declarative mapping
base = ORM_CONFIG.base

class FloorsModel(base):
    __tablename__ = 'floors'

    floor_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    building_id = Column(UUID(as_uuid=True), ForeignKey('buildings.building_id'))
    floor_name = Column(String(20))
    
    # Define the relationship with the Building table
    building = relationship("BuildingsModel", back_populates="floors")
    coordinates = relationship("FloorCoordinatesModel", back_populates="floor")
    walls = relationship("WallsModel", back_populates="floor")
    
class FloorCoordinatesModel(base):
    __tablename__ = 'floor_coordinates'

    coordinate_id = Column(Integer, primary_key=True, autoincrement=True)
    floor_id = Column(UUID(as_uuid=True), ForeignKey('floors.floor_id'))
    coordinates = Column(ARRAY(FLOAT))  # Store coordinates as an array of floats

    # Define the relationship with the FloorsModel table
    floor = relationship("FloorsModel", back_populates="coordinates")

class FloorsUtils:
    def create_floor_record(self, request_data):
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            # Create a new Floor object
            new_floor = FloorsModel(
                floor_id=uuid.uuid4(),  # Generate UUID for floor_id
                building_id=uuid.UUID(request_data['building_id']),  # Convert building_id to UUID
                floor_name=request_data['floor_name']
            )
            # Add the new_floor object to the session
            session.add(new_floor)
            # Commit the transaction to the database
            session.commit()
            
            # Add floor coordinates
            for coordinates in request_data.get('floor_coordinates', []):
                new_coordinate = FloorCoordinatesModel(
                    floor_id=new_floor.floor_id,
                    coordinates=coordinates
                )
                session.add(new_coordinate)
            
            # Commit the transaction to the database again to add floor coordinates
            session.commit()
            
            # Close the session
            session.close()
            print({"message": "Floor added successfully", "building": new_floor})
            return True, 201
        except DataError:
            session.rollback()
            print({"error": "Invalid data format"})
            return False, 400
        except IntegrityError:
            session.rollback()
            print({"error": "An error occurred while adding the wall:", "IntegrityError": ie})
            return False, 500
        
    def get_all_floors(self, building_id):
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            # Query all floors for the specified building_id
            floors = session.query(FloorsModel).filter_by(building_id=building_id).all()
            
            

            # Convert floors data to a dictionary format
            floor_data = []
            for floor in floors:
                floor_dict = {
                    "floor_id": floor.floor_id,
                    "floor_name": floor.floor_name,
                    "floor_coordinates": [],
                    # Add other floor attributes if needed
                }

                # Query floor coordinates for the current floor
                coordinates = session.query(FloorCoordinatesModel).filter_by(floor_id=floor.floor_id).all()
                
                # Include floor coordinates in the floor dictionary
                for coord in coordinates:
                    floor_dict["floor_coordinates"].append(coord.coordinates)

                floor_data.append(floor_dict)

            # Return the floor data
            session.close()
            return True, floor_data
        except Exception as e:
            # Handle any exceptions
            session.rollback()
            print({"error": "An error occurred while getting floor records", "Exception": e})
            return False, None
        
    def move_floor_coordinates_by(self, x, y, z, floor_id):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            floor_coordinates = session.query(FloorCoordinatesModel).filter_by(floor_id=floor_id).all()
            if not floor_coordinates:
                print("No floor coordinates found for the specified floor_id")
                return False, 404

            # Iterate over the records, update coordinates, and store in a dictionary
            updated_coordinates = {}
            for coord in floor_coordinates:
                updated_x = coord.coordinates[0] + x
                updated_y = coord.coordinates[1] + y
                updated_z = coord.coordinates[2] + z
                updated_coordinates[coord.coordinate_id] = {"x": updated_x, "y": updated_y, "z": updated_z}

            # Update records using the dictionary
            for coordinate_id, updated_values in updated_coordinates.items():
                session.query(FloorCoordinatesModel).filter_by(coordinate_id=coordinate_id).update(
                    {"coordinates": [updated_values["x"], updated_values["y"], updated_values["z"]]},
                    synchronize_session=False
                )

            # Commit changes to the database
            session.commit()
            print("Floor coordinates moved successfully")
            return True, 200

        except IntegrityError:
            session.rollback()
            print("An error occurred while moving floor coordinates")
            return False, 500
        finally:
            session.close()
    
    def rotate_floor_coordinates_by(self, theta_x, theta_y, theta_z, floor_id):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            # Fetch floor coordinates records
            floor_coordinates = session.query(FloorCoordinatesModel).filter_by(floor_id=floor_id).all()
            if not floor_coordinates:
                print("No floor coordinates found for the specified floor_id")
                return False, 404

            # Compute the combined rotation matrix
            rotation_matrix_combined = get_3d_rotation_matrix(theta_x, theta_y, theta_z)
            
            # Iterate over the records, apply rotation, and update coordinates
            for coord in floor_coordinates:
                # Convert the coordinates to a numpy array
                rotated_coordinates = rotate_3d_coordinates(rotation_matrix_combined, coord.coordinates)
                # Apply rotation using matrix multiplication
                
                # Update the coordinates in the database
                session.query(FloorCoordinatesModel).filter_by(coordinate_id=coord.coordinate_id).update(
                    {"coordinates": rotated_coordinates},
                    synchronize_session=False
                )

            # Commit changes to the database
            session.commit()
            print("Floor coordinates rotated successfully")
            return True, 200

        except IntegrityError:
            session.rollback()
            print("An error occurred while rotating floor coordinates")
            return False, 500
        finally:
            session.close()