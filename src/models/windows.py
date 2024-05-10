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

class WindowsModel(base):
    __tablename__ = 'windows'

    window_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wall_id = Column(UUID(as_uuid=True), ForeignKey('walls.wall_id'))
    window_thickness = Column(FLOAT)
    
    # Define the relationship with the Wall table
    wall = relationship("WallsModel", back_populates="windows")
    coordinates = relationship("WindowsCoordinatesModel", back_populates="window")

class WindowsCoordinatesModel(base):
    __tablename__ = 'window_coordinates'

    coordinate_id = Column(Integer, primary_key=True, autoincrement=True)
    window_id = Column(UUID(as_uuid=True), ForeignKey('windows.window_id'))
    coordinates = Column(ARRAY(FLOAT))  # Store coordinates as an array of floats

    # Define the relationship with the WindowModel table
    window = relationship("WindowsModel", back_populates="coordinates")

class WindowsUtils:
    def create_window_record(self, request_data):
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            # Create a new Window object
            new_window = WindowsModel(
                window_id=uuid.uuid4(),  # Generate UUID for window_id
                wall_id=uuid.UUID(request_data['wall_id']),  # Convert window_id to UUID
                window_thickness=request_data['window_thickness']
            )
            # Add the new_window object to the session
            session.add(new_window)
            # Commit the transaction to the database
            session.commit()
            
            # Add window coordinates
            for coordinates in request_data.get('window_coordinates', []):
                new_coordinate = WindowsCoordinatesModel(
                    window_id=new_window.window_id,
                    coordinates=coordinates
                )
                session.add(new_coordinate)
            
            # Commit the transaction to the database again to add window coordinates
            session.commit()
            
            # Close the session
            session.close()
            print({"message": "Window added successfully", "window": new_window})
            return True, 201
        except DataError:
            session.rollback()
            print({"error": "Invalid data format"})
            return False, 400
        except IntegrityError:
            session.rollback()
            print({"error": "An error occurred while adding the window"})
            return False, 500
        
    def get_all_windows(self, wall_id):
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            # Query all Window for the specified building_id
            windows = session.query(WindowsModel).filter_by(wall_id=wall_id).all()

            # Convert windows data to a dictionary format
            window_data = []
            for window in windows:
                window_dict = {
                    "window_id": window.window_id,
                    "window_coordinates": [],
                    # Add other window attributes if needed
                }

                # Query window coordinates for the current window
                coordinates = session.query(WindowsCoordinatesModel).filter_by(window_id=window.window_id).all()
                
                # Include window coordinates in the window dictionary
                for coord in coordinates:
                    window_dict["window_coordinates"].append(coord.coordinates)

                window_data.append(window_dict)

            # Return the window data
            session.close()
            return True, window_data
        except Exception as e:
            # Handle any exceptions
            session.rollback()
            print({"error": "An error occurred while getting window records: {e}"})
            return False, None
        
    def move_window_coordinates_by(self, x, y, z, window_id):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            window_coordinates = session.query(WindowsCoordinatesModel).filter_by(window_id=window_id).all()
            if not window_coordinates:
                print("No window coordinates found for the specified window_id")
                return False, 404

            # Iterate over the records, update coordinates, and store in a dictionary
            updated_coordinates = {}
            for coord in window_coordinates:
                updated_x = coord.coordinates[0] + x
                updated_y = coord.coordinates[1] + y
                updated_z = coord.coordinates[2] + z
                updated_coordinates[coord.coordinate_id] = {"x": updated_x, "y": updated_y, "z": updated_z}

            # Update records using the dictionary
            for coordinate_id, updated_values in updated_coordinates.items():
                session.query(WindowsCoordinatesModel).filter_by(coordinate_id=coordinate_id).update(
                    {"coordinates": [updated_values["x"], updated_values["y"], updated_values["z"]]},
                    synchronize_session=False
                )

            # Commit changes to the database
            session.commit()
            print("Window coordinates moved successfully")
            return True, 200

        except IntegrityError:
            session.rollback()
            print("An error occurred while moving window coordinates")
            return False, 500
        finally:
            session.close()
    
    def rotate_window_coordinates_by(self, theta_x, theta_y, theta_z, window_id):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            # Fetch window coordinates records
            window_coordinates = session.query(WindowsCoordinatesModel).filter_by(window_id=window_id).all()
            if not window_coordinates:
                print("No window coordinates found for the specified window_id")
                return False, 404

            # Compute the combined rotation matrix
            rotation_matrix_combined = get_3d_rotation_matrix(theta_x, theta_y, theta_z)
            
            # Iterate over the records, apply rotation, and update coordinates
            for coord in window_coordinates:
                # Convert the coordinates to a numpy array
                rotated_coordinates = rotate_3d_coordinates(rotation_matrix_combined, coord.coordinates)
                # Apply rotation using matrix multiplication
                
                # Update the coordinates in the database
                session.query(WindowsCoordinatesModel).filter_by(coordinate_id=coord.coordinate_id).update(
                    {"coordinates": rotated_coordinates},
                    synchronize_session=False
                )

            # Commit changes to the database
            session.commit()
            print("Window coordinates rotated successfully")
            return True, 200

        except IntegrityError:
            session.rollback()
            print("An error occurred while rotating window coordinates")
            return False, 500
        finally:
            session.close()

    def delete_window_by_id(self, window_id):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            # Query WindowsCoordinatesModel to get coordinates related to the window_id
            coordinates_query = session.query(WindowsCoordinatesModel).filter_by(window_id=window_id)
            # Delete coordinates related to the window_id
            coordinates_query.delete()
            
            # Query WindowsModel to get window by window_id
            window_query = session.query(WindowsModel).filter_by(window_id=window_id)
            # Delete window by window_id
            window_query.delete()

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