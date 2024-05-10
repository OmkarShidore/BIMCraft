from src.core import floors_utils

REQUIRED_FLOOR_FIELDS = ['building_id', 'floor_name', 'floor_coordinates']


def add_floor_record(request_data):
    missing_parameters = [
        field for field in REQUIRED_FLOOR_FIELDS if field not in request_data or not request_data[field]]
    if missing_parameters:
        return f"Operation Failed, missing key: {missing_parameters}", 400
    result = floors_utils.create_floor_record(request_data)
    if result[0]==True:
        return "Added floor record", 201
    elif result[1]==400:
        return "building id not found", 400
    elif result[1]==500:
        return "Operation Failed", 500


def get_floor_records(building_id):
    floor_records = floors_utils.get_all_floors(building_id)
    if not floor_records[0]:
        return f"Operation Failed", 500
    else:
        return floor_records[1]

def move_floor_coordinates(request_data):
    x = request_data.get('x', 0)
    y = request_data.get('y', 0)
    z = request_data.get('z', 0)
    floor_id = request_data.get('floor_id')

    # Check for missing parameters or all zero values
    if x == 0 and y == 0 and z == 0 or not floor_id:
        return f"Missing parameters or x, y & z are 0", 400
    result = floors_utils.move_floor_coordinates_by(x, y, z, floor_id)
    if result[0]==True:
        return "Floor Moved", result[1]
    elif result[0]==False and result[1]==404:
        return "Floor or building not found", 404
    else:
        return "Operation Failed", 500

def rotate_floor_coordinates(request_data):
    theta_x = request_data.get('theta_x', 0)
    theta_y = request_data.get('theta_y', 0)
    theta_z = request_data.get('theta_z', 0)
    floor_id = request_data.get('floor_id')

    # Check for missing parameters or all zero values
    if theta_x == 0 and theta_y == 0 and theta_z == 0 or not floor_id:
        return f"Missing parameters or x, y & z are 0", 400
    result = floors_utils.rotate_floor_coordinates_by(theta_x, theta_y, theta_z, floor_id)
    if result[0]==True:
        return "Floor Rotated", result[1]
    elif result[0]==False and result[1]==404:
        return "Floor or building not found", 404
    else:
        return "Operation Failed", 500
    