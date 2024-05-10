from src.bim_core import walls_utils

REQUIRED_WALL_FIELDS = ['floor_id', 'wall_coordinates', 'wall_thickness']

def add_wall_record(request_data):
    missing_parameters = [
        field for field in REQUIRED_WALL_FIELDS if field not in request_data or not request_data[field]]
    if missing_parameters:
        return f"Operation Failed, missing key: {missing_parameters}", 400
    result = walls_utils.create_wall_record(request_data)
    if result[0]==True:
        return "Added wall record", 201
    elif result[1]==400:
        return "building id not found", 400
    elif result[1]==500:
        return "Operation Failed", 500


def get_wall_records(building_id):
    wall_records = walls_utils.get_all_walls(building_id)
    if not wall_records[0]:
        return f"Operation Failed", 500
    else:
        return wall_records[1]

def move_wall_coordinates(request_data):
    x = request_data.get('x', 0)
    y = request_data.get('y', 0)
    z = request_data.get('z', 0)
    wall_id = request_data.get('wall_id')

    # Check for missing parameters or all zero values
    if x == 0 and y == 0 and z == 0 or not wall_id:
        return f"Missing parameters or x, y & z are 0", 400
    result = walls_utils.move_wall_coordinates_by(x, y, z, wall_id)
    if result[0]==True:
        return "Wall Moved", result[1]
    elif result[0]==False and result[1]==404:
        return "Wall or building not found", 404
    else:
        return "Operation Failed", 500

def rotate_wall_coordinates(request_data):
    theta_x = request_data.get('theta_x', 0)
    theta_y = request_data.get('theta_y', 0)
    theta_z = request_data.get('theta_z', 0)
    wall_id = request_data.get('wall_id')

    # Check for missing parameters or all zero values
    if theta_x == 0 and theta_y == 0 and theta_z == 0 or not wall_id:
        return f"Missing parameters or theta_x, theta_y & theta_z are 0", 400
    result = walls_utils.rotate_wall_coordinates_by(theta_x, theta_y, theta_z, wall_id)
    if result[0]==True:
        return "Wall Rotated", result[1]
    elif result[0]==False and result[1]==404:
        return "Wall or building not found", 404
    else:
        return "Operation Failed", 500