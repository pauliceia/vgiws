-- access postgres
sudo -i -u postgres
psql -d postgres

-- remove the database if it exists
DROP DATABASE IF EXISTS db_pauliceia_test;

-- create databse
CREATE DATABASE db_pauliceia_test;

-- connect on database
\c db_pauliceia_test

-- active the extension
CREATE EXTENSION postgis;

-- exit
\q

-- connect on database
psql -d db_pauliceia_test
