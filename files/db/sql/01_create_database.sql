-- access postgres
sudo -i -u postgres
psql -d postgres

-- remove the database if it exists
DROP DATABASE IF EXISTS pauliceia_test;

-- create databse
CREATE DATABASE pauliceia_test;

-- connect on database
\c pauliceia_test

-- active the extension
CREATE EXTENSION postgis;

-- exit
\q

-- connect on database
psql -d pauliceia_test
