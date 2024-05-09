-- 
-- CREATE DATABASE dbname;
-- CREATE USER user WITH PASSWORD 'password';
-- GRANT all ON DATABASE dbname TO dbuser;
-- \c dbname;

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

-- Insert dummy data into the buildings table
INSERT INTO buildings (name, description, owner_history, address_lines, postal_box, town, region, postal_code, country) 
VALUES 
    ('Dummy Building', 'This is a dummy building', 'Owner A', '123 Main St', 123, 'Dummy Town', 'Dummy Region', 12345, 'Dummy Country'),
    ('Dummy1 Building', 'This is a dummy building1', 'Owner B', '456 Elm St', 456, 'Dummyville', 'Dummyland', 54321, 'Dummylandia');