--psql -U postgres
CREATE DATABASE buildcraftdb;
CREATE USER buildcraftuser WITH PASSWORD 'buildcraftpassword';
GRANT all ON DATABASE buildcraftdb TO buildcraftuser;
\c buildcraftdb;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create the buildings table
CREATE TABLE buildings (
    building_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100),
    description TEXT,
    owner_history VARCHAR(20),
    address_lines VARCHAR(50),
    postal_box INTEGER,
    town VARCHAR(20),
    region VARCHAR(20),
    postal_code INTEGER,
    country VARCHAR(20)
);

-- Create the Floors table
CREATE TABLE floors (
    floor_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    building_id UUID REFERENCES buildings(building_id),
    floor_name VARCHAR(20)
);

-- Create the FloorCoordinates table
CREATE TABLE floor_coordinates (
    coordinate_id SERIAL PRIMARY KEY,
    floor_id UUID REFERENCES floors(floor_id),
    coordinates FLOAT[]  -- Store coordinates as an array of floats
);

-- Walls
CREATE TABLE walls (
    wall_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    floor_id UUID REFERENCES floors(floor_id),
    wall_thickness FLOAT
);

CREATE TABLE wall_coordinates (
    coordinate_id SERIAL PRIMARY KEY,
    wall_id UUID REFERENCES walls(wall_id),
    coordinates FLOAT[]
);

SELECT * FROM floor_coordinates;
SELECT * FROM floors;
SELECT * FROM wall_coordinates;
SELECT * FROM walls;

DELETE FROM floor_coordinates;
DELETE FROM wall_coordinates;
DELETE FROM walls;
DELETE FROM floors;

-- Insert dummy data into the buildings table
INSERT INTO buildings (name, description, owner_history, address_lines, postal_box, town, region, postal_code, country) 
VALUES 
    ('Dummy Building', 'This is a dummy building', 'Owner A', '123 Main St', 123, 'Dummy Town', 'Dummy Region', 12345, 'Dummy Country'),
    ('Dummy1 Building', 'This is a dummy building1', 'Owner B', '456 Elm St', 456, 'Dummyville', 'Dummyland', 54321, 'Dummylandia');