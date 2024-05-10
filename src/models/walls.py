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

class WallsModel(base):
    __tablename__ = 'walls'

    wall_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    floor_id = Column(UUID(as_uuid=True), ForeignKey('floors.floor_id'))
    wall_thickness = Column(FLOAT)
    
    # Define the relationship with the Floor table
    floor = relationship("FloorsModel", back_populates="walls")
    doors = relationship("DoorsModel", back_populates="wall")
    windows = relationship("WindowsModel", back_populates="wall")
    coordinates = relationship("WallCoordinatesModel", back_populates="wall")

class WallCoordinatesModel(base):
    __tablename__ = 'wall_coordinates'

    coordinate_id = Column(Integer, primary_key=True, autoincrement=True)
    wall_id = Column(UUID(as_uuid=True), ForeignKey('walls.wall_id'))
    coordinates = Column(ARRAY(FLOAT))  # Store coordinates as an array of floats

    # Define the relationship with the WallsModel table
    wall = relationship("WallsModel", back_populates="coordinates")

class WallsUtils:
    def create_wall_record(self, request_data):
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            # Create a new Wall object
            new_wall = WallsModel(
                wall_id=uuid.uuid4(),  # Generate UUID for wall_id
                floor_id=uuid.UUID(request_data['floor_id']),  # Convert floor_id to UUID
                wall_thickness=request_data['wall_thickness']
            )
            # Add the new_wall object to the session
            session.add(new_wall)
            # Commit the transaction to the database
            session.commit()
            
            # Add wall coordinates
            for coordinates in request_data.get('wall_coordinates', []):
                new_coordinate = WallCoordinatesModel(
                    wall_id=new_wall.wall_id,
                    coordinates=coordinates
                )
                session.add(new_coordinate)
            
            # Commit the transaction to the database again to add wall coordinates
            session.commit()
            
            # Close the session
            session.close()
            print({"message": "Wall added successfully", "Wall": new_wall})
            return True, 201
        except DataError:
            session.rollback()
            print({"error": "Invalid data format"})
            return False, 400
        except IntegrityError as ie:
            session.rollback()
            print({"error": "An error occurred while adding the wall:", "IntegrityError": ie})
            return False, 500
        
    def get_all_walls(self, floor_id):
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            # Query all walls for the specified building_id
            walls = session.query(WallsModel).filter_by(floor_id=floor_id).all()

            # Convert walls data to a dictionary format
            wall_data = []
            for wall in walls:
                wall_dict = {
                    "wall_id": wall.wall_id,
                    "wall_coordinates": [],
                    # Add other wall attributes if needed
                }

                # Query wall coordinates for the current wall
                coordinates = session.query(WallCoordinatesModel).filter_by(wall_id=wall.wall_id).all()
                
                # Include wall coordinates in the wall dictionary
                for coord in coordinates:
                    wall_dict["wall_coordinates"].append(coord.coordinates)

                wall_data.append(wall_dict)

            # Return the wall data
            session.close()
            return True, wall_data
        except Exception as e:
            # Handle any exceptions
            session.rollback()
            print({"error": "An error occurred while getting wall records: {e}"})
            return False, None
        
    def move_wall_coordinates_by(self, x, y, z, wall_id):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            wall_coordinates = session.query(WallCoordinatesModel).filter_by(wall_id=wall_id).all()
            if not wall_coordinates:
                print("No wall coordinates found for the specified wall_id")
                return False, 404

            # Iterate over the records, update coordinates, and store in a dictionary
            updated_coordinates = {}
            for coord in wall_coordinates:
                updated_x = coord.coordinates[0] + x
                updated_y = coord.coordinates[1] + y
                updated_z = coord.coordinates[2] + z
                updated_coordinates[coord.coordinate_id] = {"x": updated_x, "y": updated_y, "z": updated_z}

            # Update records using the dictionary
            for coordinate_id, updated_values in updated_coordinates.items():
                session.query(WallCoordinatesModel).filter_by(coordinate_id=coordinate_id).update(
                    {"coordinates": [updated_values["x"], updated_values["y"], updated_values["z"]]},
                    synchronize_session=False
                )

            # Commit changes to the database
            session.commit()
            print("Wall coordinates moved successfully")
            return True, 200

        except IntegrityError:
            session.rollback()
            print("An error occurred while moving wall coordinates")
            return False, 500
        finally:
            session.close()
    
    def rotate_wall_coordinates_by(self, theta_x, theta_y, theta_z, wall_id):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            # Fetch wall coordinates records
            wall_coordinates = session.query(WallCoordinatesModel).filter_by(wall_id=wall_id).all()
            if not wall_coordinates:
                print("No wall coordinates found for the specified wall_id")
                return False, 404

            # Compute the combined rotation matrix
            rotation_matrix_combined = get_3d_rotation_matrix(theta_x, theta_y, theta_z)
            
            # Iterate over the records, apply rotation, and update coordinates
            for coord in wall_coordinates:
                # Convert the coordinates to a numpy array
                rotated_coordinates = rotate_3d_coordinates(rotation_matrix_combined, coord.coordinates)
                # Apply rotation using matrix multiplication
                
                # Update the coordinates in the database
                session.query(WallCoordinatesModel).filter_by(coordinate_id=coord.coordinate_id).update(
                    {"coordinates": rotated_coordinates},
                    synchronize_session=False
                )

            # Commit changes to the database
            session.commit()
            print("Wall coordinates rotated successfully")
            return True, 200

        except IntegrityError:
            session.rollback()
            print("An error occurred while rotating wall coordinates")
            return False, 500
        finally:
            session.close()