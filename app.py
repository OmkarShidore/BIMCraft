from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.config import APP_CONFIG
from src.core.buildings import get_building_records

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

@app.route('/list_projects')
def list_projects():
    result = get_building_records()
    return result

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5001)
