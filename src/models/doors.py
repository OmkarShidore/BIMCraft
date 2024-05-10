from sqlalchemy.orm import relationship
from sqlalchemy import Column, ARRAY, Integer, ForeignKey
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

class DoorsModel(base):
    __tablename__ = 'doors'

    door_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wall_id = Column(UUID(as_uuid=True), ForeignKey('walls.wall_id'))
    door_thickness = Column(FLOAT)
    
    # Define the relationship with the Wall table
    wall = relationship("WallsModel", back_populates="doors")
    coordinates = relationship("DoorCoordinatesModel", back_populates="door")

class DoorCoordinatesModel(base):
    __tablename__ = 'door_coordinates'

    coordinate_id = Column(Integer, primary_key=True, autoincrement=True)
    door_id = Column(UUID(as_uuid=True), ForeignKey('doors.door_id'))
    coordinates = Column(ARRAY(FLOAT))  # Store coordinates as an array of floats

    # Define the relationship with the DoorModel table
    door = relationship("DoorsModel", back_populates="coordinates")

class DoorsUtils:
    def create_door_record(self, request_data):
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            # Create a new Door object
            new_door = DoorsModel(
                door_id=uuid.uuid4(),  # Generate UUID for door_id
                wall_id=uuid.UUID(request_data['wall_id']),  # Convert door_id to UUID
                door_thickness=request_data['door_thickness']
            )
            # Add the new_door object to the session
            session.add(new_door)
            # Commit the transaction to the database
            session.commit()
            
            # Add door coordinates
            for coordinates in request_data.get('door_coordinates', []):
                new_coordinate = DoorCoordinatesModel(
                    door_id=new_door.door_id,
                    coordinates=coordinates
                )
                session.add(new_coordinate)
            
            # Commit the transaction to the database again to add door coordinates
            session.commit()
            
            # Close the session
            session.close()
            print({"message": "Door added successfully", "door": new_door})
            return True, 201
        except DataError:
            session.rollback()
            print({"error": "Invalid data format"})
            return False, 400
        except IntegrityError:
            session.rollback()
            print({"error": "An error occurred while adding the door"})
            return False, 500
        
    def get_all_doors(self, wall_id):
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            # Query all doors for the specified building_id
            doors = session.query(DoorsModel).filter_by(wall_id=wall_id).all()

            # Convert doors data to a dictionary format
            door_data = []
            for door in doors:
                door_dict = {
                    "door_id": door.door_id,
                    "door_coordinates": [],
                    # Add other door attributes if needed
                }

                # Query door coordinates for the current door
                coordinates = session.query(DoorCoordinatesModel).filter_by(door_id=door.door_id).all()
                
                # Include door coordinates in the door dictionary
                for coord in coordinates:
                    door_dict["door_coordinates"].append(coord.coordinates)

                door_data.append(door_dict)

            # Return the door data
            session.close()
            return True, door_data
        except Exception as e:
            # Handle any exceptions
            session.rollback()
            print({"error": "An error occurred while getting door records: {e}"})
            return False, None
        
    def move_door_coordinates_by(self, x, y, z, door_id):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            door_coordinates = session.query(DoorCoordinatesModel).filter_by(door_id=door_id).all()
            if not door_coordinates:
                print("No door coordinates found for the specified door_id")
                return False, 404

            # Iterate over the records, update coordinates, and store in a dictionary
            updated_coordinates = {}
            for coord in door_coordinates:
                updated_x = coord.coordinates[0] + x
                updated_y = coord.coordinates[1] + y
                updated_z = coord.coordinates[2] + z
                updated_coordinates[coord.coordinate_id] = {"x": updated_x, "y": updated_y, "z": updated_z}

            # Update records using the dictionary
            for coordinate_id, updated_values in updated_coordinates.items():
                session.query(DoorCoordinatesModel).filter_by(coordinate_id=coordinate_id).update(
                    {"coordinates": [updated_values["x"], updated_values["y"], updated_values["z"]]},
                    synchronize_session=False
                )

            # Commit changes to the database
            session.commit()
            print("Door coordinates moved successfully")
            return True, 200

        except IntegrityError:
            session.rollback()
            print("An error occurred while moving door coordinates")
            return False, 500
        finally:
            session.close()
    
    def rotate_door_coordinates_by(self, theta_x, theta_y, theta_z, door_id):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            # Fetch door coordinates records
            door_coordinates = session.query(DoorCoordinatesModel).filter_by(door_id=door_id).all()
            if not door_coordinates:
                print("No door coordinates found for the specified door_id")
                return False, 404

            # Compute the combined rotation matrix
            rotation_matrix_combined = get_3d_rotation_matrix(theta_x, theta_y, theta_z)
            
            # Iterate over the records, apply rotation, and update coordinates
            for coord in door_coordinates:
                # Convert the coordinates to a numpy array
                rotated_coordinates = rotate_3d_coordinates(rotation_matrix_combined, coord.coordinates)
                # Apply rotation using matrix multiplication
                
                # Update the coordinates in the database
                session.query(DoorCoordinatesModel).filter_by(coordinate_id=coord.coordinate_id).update(
                    {"coordinates": rotated_coordinates},
                    synchronize_session=False
                )

            # Commit changes to the database
            session.commit()
            print("Door coordinates rotated successfully")
            return True, 200

        except IntegrityError:
            session.rollback()
            print("An error occurred while rotating door coordinates")
            return False, 500
        finally:
            session.close()

    def delete_door_by_id(self, door_id):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            # Query DoorsCoordinatesModel to get coordinates related to the door_id
            coordinates_query = session.query(DoorCoordinatesModel).filter_by(door_id=door_id)
            # Delete coordinates related to the door_id
            coordinates_query.delete()
            
            # Query DoorModel to get door by door_id
            door_query = session.query(DoorsModel).filter_by(door_id=door_id)
            # Delete door by door_id
            door_query.delete()

            # Commit the transaction
            session.commit()
            print("Record deleted successfully.")
            return True, 200
        except IntegrityError:
            session.rollback()
            print("An error occurred while delete door records")
            return False, 500
        finally:
            session.close()