-- sudo -u postgres psql
SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

CREATE DATABASE buildcraftdb;
CREATE USER buildcraftuser WITH PASSWORD 'buildcraftpassword';
GRANT all ON DATABASE buildcraftdb TO buildcraftuser;
\c buildcraftdb;

SET SCHEMA 'public';
CREATE EXTENSION vector;