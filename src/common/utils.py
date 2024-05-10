import numpy as np

def get_3d_rotation_matrix(theta_x, theta_y, theta_z):
    theta_x_rad = np.radians(theta_x)
    theta_y_rad = np.radians(theta_y)
    theta_z_rad = np.radians(theta_z)

    # Define rotation matrices for each axis
    rotation_matrix_x = np.array([
        [1, 0, 0],
        [0, np.cos(theta_x_rad), -np.sin(theta_x_rad)],
        [0, np.sin(theta_x_rad), np.cos(theta_x_rad)]
    ])

    rotation_matrix_y = np.array([
        [np.cos(theta_y_rad), 0, np.sin(theta_y_rad)],
        [0, 1, 0],
        [-np.sin(theta_y_rad), 0, np.cos(theta_y_rad)]
    ])

    rotation_matrix_z = np.array([
        [np.cos(theta_z_rad), -np.sin(theta_z_rad), 0],
        [np.sin(theta_z_rad), np.cos(theta_z_rad), 0],
        [0, 0, 1]
    ])

    # Compute the combined rotation matrix
    rotation_matrix_combined = np.dot(rotation_matrix_z, np.dot(rotation_matrix_y, rotation_matrix_x))

    return rotation_matrix_combined

def rotate_3d_coordinates(rotation_matrix, coordinates):
    np_coordinates = np.array(coordinates)
    rotated_coordinates = np.dot(rotation_matrix, np_coordinates)
    
    return rotated_coordinates.tolist()