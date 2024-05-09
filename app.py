from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from src.config import APP_CONFIG
from src.core.buildings import get_building_records, add_building_record
from src.core.floors import get_floor_records, add_floor_record, move_floor_coordinates, rotate_floor_coordinates

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

@app.route('/get_buildings')
def get_buildings():
    result = get_building_records()
    return result

@app.route('/add_building', methods=["POST"])
def add_building():
    request_data = request.json
    result = add_building_record(request_data)
    return result

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

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5001)
