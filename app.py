from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from src.config import APP_CONFIG
from src.bim_core.buildings import get_building_records, add_building_record
from src.bim_core.floors import get_floor_records, add_floor_record, move_floor_coordinates, rotate_floor_coordinates
from src.bim_core.walls import get_wall_records, add_wall_record, move_wall_coordinates, rotate_wall_coordinates
from src.bim_core.doors import get_door_records, add_door_record, move_door_coordinates, rotate_door_coordinates
from src.bim_core.windows import get_window_records, add_window_record, move_window_coordinates, rotate_window_coordinates


db_name = APP_CONFIG.POSTGRES_DB
username = APP_CONFIG.POSTGRES_USER
password = APP_CONFIG.POSTGRES_PASSWORD
host = APP_CONFIG.POSTGRES_HOST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@{host}:5432/{db_name}"
db = SQLAlchemy(app)

class Building(db.Model):
    __tablename__ = 'buildings'
    building_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)

@app.route('/health')
def health():
    return "OK"

#-----Buildings

@app.route('/get_buildings')
def get_buildings():
    result = get_building_records()
    return result

@app.route('/add_building', methods=["POST"])
def add_building():
    request_data = request.json
    result = add_building_record(request_data)
    return result

#-----Floors

@app.route('/get_floors', methods=["GET"])
def get_floors():
    building_id = request.args.get('building_id')
    if not building_id:
        return jsonify({"error": "building_id parameter is missing"}), 400
    result = get_floor_records(building_id)
    return result

@app.route('/add_floor', methods=["POST"])
def add_floor():
    request_data = request.json
    result = add_floor_record(request_data)
    return result

@app.route('/move_floor', methods=["POST"])
def move_floor():
    request_data = request.json
    result = move_floor_coordinates(request_data)
    return result

@app.route('/rotate_floor', methods=["POST"])
def rotate_floor():
    request_data = request.json
    result = rotate_floor_coordinates(request_data)
    return result

#----Walls

@app.route('/get_walls', methods=["GET"])
def get_walls():
    floor_id = request.args.get('floor_id')
    if not floor_id:
        return jsonify({"error": "floor_id parameter is missing"}), 400
    result = get_wall_records(floor_id)
    return result

@app.route('/add_wall', methods=["POST"])
def add_wall():
    request_data = request.json
    result = add_wall_record(request_data)
    return result

@app.route('/move_wall', methods=["POST"])
def move_wall():
    request_data = request.json
    result = move_wall_coordinates(request_data)
    return result

@app.route('/rotate_wall', methods=["POST"])
def rotate_wall():
    request_data = request.json
    result = rotate_wall_coordinates(request_data)
    return result

#----Doors

@app.route('/get_doors', methods=["GET"])
def get_doors():
    wall_id = request.args.get('wall_id')
    if not wall_id:
        return jsonify({"error": "wall_id parameter is missing"}), 400
    result = get_door_records(wall_id)
    return result

@app.route('/add_door', methods=["POST"])
def add_door():
    request_data = request.json
    result = add_door_record(request_data)
    return result

@app.route('/move_door', methods=["POST"])
def move_door():
    request_data = request.json
    result = move_door_coordinates(request_data)
    return result

@app.route('/rotate_door', methods=["POST"])
def rotate_door():
    request_data = request.json
    result = rotate_door_coordinates(request_data)
    return result

#----Windows

@app.route('/get_windows', methods=["GET"])
def get_windows():
    wall_id = request.args.get('wall_id')
    if not wall_id:
        return jsonify({"error": "wall_id parameter is missing"}), 400
    result = get_window_records(wall_id)
    return result

@app.route('/add_window', methods=["POST"])
def add_window():
    request_data = request.json
    result = add_window_record(request_data)
    return result

@app.route('/move_window', methods=["POST"])
def move_window():
    request_data = request.json
    result = move_window_coordinates(request_data)
    return result

@app.route('/rotate_window', methods=["POST"])
def rotate_window():
    request_data = request.json
    result = rotate_window_coordinates(request_data)
    return result

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5001)
