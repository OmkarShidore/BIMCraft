from src.bim_core import windows_utils

REQUIRED_WALL_FIELDS = ['wall_id', 'window_coordinates', 'window_thickness']

def add_window_record(request_data):
    missing_parameters = [
        field for field in REQUIRED_WALL_FIELDS if field not in request_data or not request_data[field]]
    if missing_parameters:
        return f"Operation Failed, missing key: {missing_parameters}", 400
    result = windows_utils.create_window_record(request_data)
    if result[0]==True:
        return "Added window record", 201
    elif result[1]==400:
        return "window id not found", 400
    elif result[1]==500:
        return "Operation Failed", 500


def get_window_records(wall_id):
    window_records = windows_utils.get_all_windows(wall_id)
    if not window_records[0]:
        return f"Operation Failed", 500
    else:
        return window_records[1]

def move_window_coordinates(request_data):
    x = request_data.get('x', 0)
    y = request_data.get('y', 0)
    z = request_data.get('z', 0)
    window_id = request_data.get('window_id')

    # Check for missing parameters or all zero values
    if x == 0 and y == 0 and z == 0 or not window_id:
        return f"Missing parameters or x, y & z are 0", 400
    result = windows_utils.move_window_coordinates_by(x, y, z, window_id)
    if result[0]==True:
        return "Wall Moved", result[1]
    elif result[0]==False and result[1]==404:
        return "Window not found", 404
    else:
        return "Operation Failed", 500

def rotate_window_coordinates(request_data):
    theta_x = request_data.get('theta_x', 0)
    theta_y = request_data.get('theta_y', 0)
    theta_z = request_data.get('theta_z', 0)
    window_id = request_data.get('window_id')

    # Check for missing parameters or all zero values
    if theta_x == 0 and theta_y == 0 and theta_z == 0 or not window_id:
        return f"Missing parameters or theta_x, theta_y & theta_z are 0", 400
    result = windows_utils.rotate_window_coordinates_by(theta_x, theta_y, theta_z, window_id)
    if result[0]==True:
        return "Window Rotated", result[1]
    elif result[0]==False and result[1]==404:
        return "Window not found", 404
    else:
        return "Operation Failed", 500
    
def delete_window_record(window_id):
    result = windows_utils.delete_window_by_id(window_id)
    if result[0]==True:
        return "Window deleted", result[1]
    else:
        return "Operation Failed", 500
