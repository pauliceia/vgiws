-- -----------------------------------------------------
-- Table pauliceia_user
-- -----------------------------------------------------
-- clean user table
DELETE FROM pauliceia_user;

-- add users
-- PS: the passwords are in sha512 hash

-- password - admin
INSERT INTO pauliceia_user (user_id, username, email, password, name, created_at, is_email_valid, terms_agreed, login_date, is_the_admin, receive_notification_by_email, picture, social_id, social_account)
VALUES (1001, 'admin', 'admin@admin.com', 'c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec',
'Administrator', '2017-01-01', TRUE, TRUE, '2017-01-01', TRUE, TRUE, '', '', '');

-- password - rodrigo
INSERT INTO pauliceia_user (user_id, username, email, password, name, created_at, is_email_valid, terms_agreed, login_date, is_the_admin, receive_notification_by_email, picture, social_id, social_account)
VALUES (1002, 'rodrigo', 'rodrigo@admin.com', '3ad7e557497e106756c44b7f3f401fd3f28f84c3c9ad989157868d03686f683f82d5cde1a096c4bbdbd76287e96e9a04d9f0ce8726b945c95f01b18361088a0d',
'Rodrigo', '2017-03-03', TRUE, TRUE, '2017-03-03', TRUE, TRUE, '', '', '');

-- password - miguel
INSERT INTO pauliceia_user (user_id, username, email, password, name, created_at, is_email_valid, terms_agreed, login_date, is_the_admin, receive_notification_by_email, picture, social_id, social_account)
VALUES (1003, 'miguel', 'miguel@admin.com', 'e1fc7a4313def98ae5303b0448c89d9a5126f3239608950859f3ea6fdeb8b19f6f7c103ecf97700be851cfbf8cda756c0929498021c675c643809eeeb4ebcbda',
'Miguel', '2017-05-08', TRUE, TRUE, '2017-05-08', FALSE, TRUE, '', '', '');

-- password - rafael
INSERT INTO pauliceia_user (user_id, username, email, password, name, created_at, is_email_valid, terms_agreed, login_date, is_the_admin, receive_notification_by_email, picture, social_id, social_account)
VALUES (1004, 'rafael', 'rafael@admin.com', 'c5663337df01fe3ab80478e78963534956a7e5446d72b16db9f33a36c787954414fea6de37a02d5f32ac2fe18f010068688d707e6dd260ca1f0a255f6d2f1959',
'Rafael', '2017-06-09', TRUE, FALSE, '2017-06-09', FALSE, TRUE, '', '', '');

-- password - gabriel
INSERT INTO pauliceia_user (user_id, username, email, password, name, created_at, is_email_valid, terms_agreed, login_date, is_the_admin, receive_notification_by_email, picture, social_id, social_account)
VALUES (1005, 'gabriel', 'gabriel@admin.com', '5dbe7d079067809bb06f7c80de78ecb9d914f5735265148cd704f85353fc0b5114ebbfc960539cd3f430e7b12eb3fdc261726bb756bab9658c6db6a302913df1',
'Gabriel', '2017-09-20', FALSE, FALSE, '2017-09-20', FALSE, TRUE, '', '', '');

-- password - fernanda
INSERT INTO pauliceia_user (user_id, username, email, password, created_at, is_email_valid, terms_agreed, login_date, is_the_admin, receive_notification_by_email, picture, social_id, social_account)
VALUES (1006, 'fernanda', 'fernanda@admin.com', '50f7e79988a894dd83f61370afbf3882a80ab4215f0be088fd1197b43abb24641d2711d0ada4cdf71c29718d549a9f90f82b2a0c9e1cd4adf28c0eb79816d862',
'2017-01-19', TRUE, FALSE, '2017-01-19', FALSE, TRUE, '', '', '');

-- password - ana
INSERT INTO pauliceia_user (user_id, username, email, password, created_at, is_email_valid, terms_agreed, login_date, is_the_admin, receive_notification_by_email, picture, social_id, social_account)
VALUES (1007, 'ana', 'ana@admin.com', '40c41475561375aa28d4d035445525f0e8f6bfaba1fdb4bc0c30dec2de112d7c7df168bdced38b4d87326b4c3f226c2ba1a09f4384451b0bc5f9c108c1c1df32',
'2017-01-18', TRUE, TRUE, '2017-01-18', FALSE, FALSE, '', '', '');

-- password - bea
INSERT INTO pauliceia_user (user_id, username, email, password, created_at, is_email_valid, terms_agreed, login_date, is_the_admin, receive_notification_by_email, picture, social_id, social_account)
VALUES (1008, 'bea', 'bea@admin.com', '8f685cd8902159de33414b04d8cb93e9c5f49ddec285cf6f5d61dc425d6e0b0b5328d775320a36f3655e339fceb009ad834a3e28fcc5641eccc0c6b107dc2793',
'2017-01-30', FALSE, FALSE, '2017-01-30', FALSE, FALSE, '', '', '');


-- SELECT name FROM pauliceia_user;
-- SELECT name FROM pauliceia_user WHERE unaccent(LOWER(name)) LIKE '%' || unaccent(LOWER('êL')) || '%';



-- -----------------------------------------------------
-- Table temporal_columns
-- -----------------------------------------------------
-- clean table
DELETE FROM mask;

INSERT INTO mask (mask_id, mask) VALUES (1001, 'YYYY-MM-DD');
INSERT INTO mask (mask_id, mask) VALUES (1002, 'YYYY-MM');
INSERT INTO mask (mask_id, mask) VALUES (1003, 'YYYY');



-- -----------------------------------------------------
-- Table temporal_columns
-- -----------------------------------------------------
-- clean table
DELETE FROM temporal_columns;



-- -----------------------------------------------------
-- Table keyword
-- -----------------------------------------------------
-- clean table
DELETE FROM keyword;

INSERT INTO keyword (keyword_id, name, user_id_creator, created_at) VALUES (1001, 'generic', 1001, '2017-01-01');
INSERT INTO keyword (keyword_id, name, user_id_creator, created_at) VALUES (1002, 'event', 1001, '2017-01-01');
INSERT INTO keyword (keyword_id, name, user_id_creator, created_at) VALUES (1003, 'crime', 1002, '2017-01-01');
INSERT INTO keyword (keyword_id, name, user_id_creator, created_at) VALUES (1004, 'assault', 1002, '2017-01-01');
INSERT INTO keyword (keyword_id, name, user_id_creator, created_at) VALUES (1005, 'robbery', 1002, '2017-01-01');
INSERT INTO keyword (keyword_id, name, user_id_creator, created_at) VALUES (1010, 'disease', 1001, '2017-01-01');
INSERT INTO keyword (keyword_id, name, user_id_creator, created_at) VALUES (1020, 'object', 1001, '2017-01-01');
INSERT INTO keyword (keyword_id, name, user_id_creator, created_at) VALUES (1021, 'building', 1003, '2017-01-01');
INSERT INTO keyword (keyword_id, name, user_id_creator, created_at) VALUES (1022, 'school', 1003, '2017-01-01');
INSERT INTO keyword (keyword_id, name, user_id_creator, created_at) VALUES (1023, 'hospital', 1003, '2017-01-01');
INSERT INTO keyword (keyword_id, name, user_id_creator, created_at) VALUES (1030, 'cultural place', 1003, '2017-01-01');
INSERT INTO keyword (keyword_id, name, user_id_creator, created_at) VALUES (1031, 'cinema', 1001, '2017-01-01');
INSERT INTO keyword (keyword_id, name, user_id_creator, created_at) VALUES (1040, 'street', 1001, '2017-01-01');
INSERT INTO keyword (keyword_id, name, user_id_creator, created_at) VALUES (1041, 'address', 1001, '2017-01-01');



-- -----------------------------------------------------
-- Table curator
-- -----------------------------------------------------
-- clean table
DELETE FROM curator;

INSERT INTO curator (user_id, keyword_id, region, created_at) VALUES (1001, 1001, 'amaro', '2018-01-01');
INSERT INTO curator (user_id, keyword_id, region, created_at) VALUES (1001, 1002, 'azure', '2018-01-10');
INSERT INTO curator (user_id, keyword_id, region, created_at) VALUES (1002, 1002, 'belondres', '2018-01-10');
INSERT INTO curator (user_id, keyword_id, region, created_at) VALUES (1003, 1010, 'jorge', '2018-02-22');
INSERT INTO curator (user_id, keyword_id, region, created_at) VALUES (1003, 1020, 'centro', '2018-01-15');
INSERT INTO curator (user_id, keyword_id, region, created_at) VALUES (1004, 1003, 'são francisco', '2018-02-20');
INSERT INTO curator (user_id, keyword_id, region, created_at) VALUES (1005, 1010, 'são bento', '2018-02-22');
INSERT INTO curator (user_id, keyword_id, region, created_at) VALUES (1006, 1021, 'avenida rodônia', '2018-03-24');



-- -----------------------------------------------------
-- Table layer_keyword
-- -----------------------------------------------------
-- clean table
DELETE FROM layer_keyword;


-- -----------------------------------------------------
-- Table reference
-- -----------------------------------------------------
-- clean table
DELETE FROM reference;

INSERT INTO reference (reference_id, description, user_id_creator) VALUES (1050, 'BookA', 1001);
INSERT INTO reference (reference_id, description, user_id_creator) VALUES (1051, 'ArticleB', 1002);
INSERT INTO reference (reference_id, description, user_id_creator) VALUES (1052, 'ThesisC', 1003);
INSERT INTO reference (reference_id, description, user_id_creator) VALUES (1053, 'DissertationD', 1003);


-- -----------------------------------------------------
-- Table changeset
-- -----------------------------------------------------
-- clean table
DELETE FROM changeset;



-- -----------------------------------------------------
-- Table user_layer
-- -----------------------------------------------------
-- clean table
DELETE FROM user_layer;


-- -----------------------------------------------------
-- Table user_layer
-- -----------------------------------------------------
-- clean table
DELETE FROM layer_reference;


-- -----------------------------------------------------
-- Table user_layer
-- -----------------------------------------------------
-- clean table
DELETE FROM layer_followers;


-- -----------------------------------------------------
-- Table user_layer
-- -----------------------------------------------------
-- clean table
DELETE FROM keyword_followers;


-- -----------------------------------------------------
-- Table layer
-- -----------------------------------------------------
-- clean table
DELETE FROM layer;


-- add layer 1001
INSERT INTO layer (layer_id, f_table_name, name, description, source_description, created_at) VALUES
(1001, 'layer_1001', 'Addresses in 1869', '', '', '2017-01-01');

-- add reference
INSERT INTO reference (reference_id, description, user_id_creator) VALUES (1001,
'@Misc{jorge2017book1,
author = {Jorge},
title = {Book1},
howpublished = {\url{http://www.link.org/}},
note = {Accessed on 01/01/2017},
year={2017}
}', 1001);
INSERT INTO layer_reference (layer_id, reference_id) VALUES (1001, 1001);

INSERT INTO reference (reference_id, description, user_id_creator) VALUES (1002,
'@Misc{ana2017article2,
author = {Ana},
title = {Article2},
howpublished = {\url{http://www.myhost.org/}},
note = {Accessed on 05/02/2017},
year={2017}
}', 1001);
INSERT INTO layer_reference (layer_id, reference_id) VALUES (1001, 1002);

-- add the keywords in layer
INSERT INTO layer_keyword (layer_id, keyword_id) VALUES (1001, 1001);
INSERT INTO layer_keyword (layer_id, keyword_id) VALUES (1001, 1041);

-- create a feature table to save the data
DROP TABLE IF EXISTS layer_1001 CASCADE ;
CREATE TABLE IF NOT EXISTS layer_1001 (
  id SERIAL,
  geom GEOMETRY(MULTIPOINT, 4326) NOT NULL,
  address TEXT,
  start_date TIMESTAMP,
  end_date TIMESTAMP,
  version INT NOT NULL DEFAULT 1,
  changeset_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT constraint_fk_changeset_id
    FOREIGN KEY (changeset_id)
    REFERENCES changeset (changeset_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

DROP TABLE IF EXISTS version_layer_1001 CASCADE ;
CREATE TABLE IF NOT EXISTS version_layer_1001 (
  id SERIAL,
  geom GEOMETRY(MULTIPOINT, 4326) NOT NULL,
  address TEXT,
  start_date TIMESTAMP,
  end_date TIMESTAMP,
  version INT NOT NULL DEFAULT 1,
  changeset_id INT NOT NULL,
  is_removed BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (id, version),
  CONSTRAINT constraint_fk_changeset_id
    FOREIGN KEY (changeset_id)
    REFERENCES changeset (changeset_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- add temporal metadata
INSERT INTO temporal_columns (f_table_name, start_date_column_name, end_date_column_name, start_date, end_date, start_date_mask_id, end_date_mask_id) VALUES
('layer_1001', 'start_date', 'end_date', '1869-01-01', '1975-12-31', 1001, 1001);

-- add users in layers (the main user is added when the layer is created)
INSERT INTO user_layer (layer_id, user_id, created_at, is_the_creator) VALUES (1001, 1001, '2017-01-02', TRUE);
INSERT INTO user_layer (layer_id, user_id, created_at) VALUES (1001, 1002, '2017-01-03');


-- users can follow the layer
INSERT INTO layer_followers (layer_id, user_id, created_at) VALUES (1001, 1001, '2017-01-01');
INSERT INTO layer_followers (layer_id, user_id, created_at) VALUES (1001, 1002, '2017-01-05');
INSERT INTO layer_followers (layer_id, user_id, created_at) VALUES (1001, 1003, '2017-01-08');

-- create a changeset
INSERT INTO changeset (changeset_id, created_at, layer_id, user_id_creator) VALUES (1001, '2017-01-05', 1001, 1001);

-- insert the data into the layer
INSERT INTO layer_1001 (id, geom, address, start_date, end_date, changeset_id) VALUES
(1001, ST_GeomFromText('MULTIPOINT((-46.6375790530164 -23.5290461960682))', 4326), 'R. São José', '1869-01-01', '1869-12-31', 1001);
INSERT INTO layer_1001 (id, geom, address, start_date, end_date, changeset_id) VALUES
(1002, ST_GeomFromText('MULTIPOINT((-46.6498716962487 -23.5482894062877))', 4326), 'R. Marechal Deodoro', '1869-01-01', '1869-12-31', 1001);
-- add data as GeoJSON
INSERT INTO layer_1001 (id, geom, start_date, end_date, changeset_id)
VALUES (1003,
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiPoint",
		    "coordinates":[[-46.6468896156385, -23.5494865576549]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	),
	'1875-01-01', '1875-12-31', 1001);

-- close the changeset
UPDATE changeset SET closed_at='2017-01-05', description='Creating layer_1001' WHERE changeset_id=1001;

-- create a open changeset
INSERT INTO changeset (changeset_id, description, created_at, layer_id, user_id_creator) VALUES (1011, 'An open changeset', '2017-01-08', 1001, 1001);

-- check if the layer has features and check if the changeset was created
/*
SELECT * FROM layer_1001;
SELECT * FROM version_layer_1001;
SELECT * FROM changeset WHERE id=1001;
*/



-- add layer 1002
INSERT INTO layer (layer_id, f_table_name, name, description, source_description, created_at) VALUES
(1002, 'layer_1002', 'Robberies between 1880 to 1900', '', '', '2017-03-05');

-- add reference
INSERT INTO reference (reference_id, description, user_id_creator) VALUES (1005,
'@Misc{marco2017articleB,
author = {Marco},
title = {ArticleB},
howpublished = {\url{http://www.link_to_document.org/}},
note = {Accessed on 02/02/2017},
year={2017}
}', 1001);
INSERT INTO layer_reference (layer_id, reference_id) VALUES (1002, 1005);

-- add the keywords in layer
INSERT INTO layer_keyword (layer_id, keyword_id) VALUES (1002, 1010);

-- create a feature table to save the data
--DROP TABLE IF EXISTS layer_1002 CASCADE ;
DROP TABLE IF EXISTS layer_1002 CASCADE ;
CREATE TABLE IF NOT EXISTS layer_1002 (
  id SERIAL,
  geom GEOMETRY(MULTIPOINT, 4326) NOT NULL,
  address TEXT,
  start_date TIMESTAMP,
  end_date TEXT,
  version INT NOT NULL DEFAULT 1,
  changeset_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT constraint_fk_changeset_id
    FOREIGN KEY (changeset_id)
    REFERENCES changeset (changeset_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

--DROP TABLE IF EXISTS version_layer_1002 CASCADE ;
DROP TABLE IF EXISTS version_layer_1002 CASCADE ;
CREATE TABLE IF NOT EXISTS version_layer_1002 (
  id SERIAL,
  geom GEOMETRY(MULTIPOINT, 4326) NOT NULL,
  address TEXT,
  start_date TIMESTAMP,
  end_date TEXT,
  version INT NOT NULL DEFAULT 1,
  changeset_id INT NOT NULL,
  is_removed BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (id, version),
  CONSTRAINT constraint_fk_changeset_id
    FOREIGN KEY (changeset_id)
    REFERENCES changeset (changeset_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- add temporal metadata
INSERT INTO temporal_columns (f_table_name, start_date_column_name, end_date_column_name, start_date, end_date, start_date_mask_id, end_date_mask_id) VALUES
('layer_1002', 'start_date', 'end_date', '1886-01-01', '1890-12-31', 1001, 1001);

-- add users in layers (the main user is added when the layer is created)
INSERT INTO user_layer (layer_id, user_id, created_at, is_the_creator) VALUES (1002, 1001, '2017-03-05', TRUE);
INSERT INTO user_layer (layer_id, user_id, created_at) VALUES (1002, 1004, '2017-03-05');

-- users that follow the layer
INSERT INTO layer_followers (layer_id, user_id, created_at) VALUES (1002, 1001, '2017-01-02');
INSERT INTO layer_followers (layer_id, user_id, created_at) VALUES (1002, 1003, '2017-01-02');
INSERT INTO layer_followers (layer_id, user_id, created_at) VALUES (1002, 1005, '2017-01-02');

-- create a changeset
INSERT INTO changeset (changeset_id, created_at, layer_id, user_id_creator) VALUES (1002, '2017-03-05', 1002, 1004);

-- insert the data into the layer
INSERT INTO layer_1002 (id, geom, address, start_date, end_date, changeset_id) VALUES
(1006, ST_GeomFromText('MULTIPOINT((-46.6484982955712 -23.5492054322931))', 4326), 'R. 11 de Junho, 9 = D. José de Barros', '1886-02-03', '', 1002);
INSERT INTO layer_1002 (id, geom, address, start_date, end_date, changeset_id) VALUES
(1007, ST_GeomFromText('MULTIPOINT((-46.6526581134833 -23.5401195274321))', 4326), 'R. 15 de Novembro, 17A', '1890-03-04', '', 1002);
INSERT INTO layer_1002 (id, geom, address, start_date, end_date, changeset_id) VALUES
(1008, ST_GeomFromText('MULTIPOINT((-46.6466156443949 -23.5289798845685))', 4326), 'R. Barra Funda, 74', '1897-02-05', '', 1002);
-- add data as GeoJSON
INSERT INTO layer_1002 (id, geom, start_date, end_date, changeset_id)
VALUES (1009,
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiPoint",
		    "coordinates":[[-46.6531421851224, -23.5427759121502]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	),
	'1897-12-10', '', 1002);

-- close the changeset
UPDATE changeset SET closed_at='2017-03-05', description='Creating layer_1002' WHERE changeset_id=1002;

-- create a open changeset
INSERT INTO changeset (changeset_id, description, created_at, layer_id, user_id_creator) VALUES (1014, 'An open changeset', '2017-01-08', 1002, 1004);

-- check if the layer has features and check if the changeset was created
/*
SELECT * FROM layer_1002;
SELECT * FROM version_layer_1002;
SELECT * FROM changeset WHERE id=1002;
*/



-- add layer_1003
INSERT INTO layer (layer_id, f_table_name, name, description, source_description, created_at) VALUES
(1003, 'layer_1003', 'Streets in 1930', '', '', '2017-04-10');

-- add reference
INSERT INTO reference (reference_id, description, user_id_creator) VALUES (1010,
'@Misc{marco2017articleC,
author = {Marco},
title = {ArticleC},
howpublished = {\url{http://www.link_to_document.org/}},
note = {Accessed on 02/02/2017},
year={2017}
}', 1005);
INSERT INTO layer_reference (layer_id, reference_id) VALUES (1003, 1010);

-- add the keywords in layer
INSERT INTO layer_keyword (layer_id, keyword_id) VALUES (1003, 1001);
INSERT INTO layer_keyword (layer_id, keyword_id) VALUES (1003, 1040);

-- create a feature table to save the data
--DROP TABLE IF EXISTS layer_1003 CASCADE ;
DROP TABLE IF EXISTS layer_1003 CASCADE ;
CREATE TABLE IF NOT EXISTS layer_1003 (
  id SERIAL,
  geom GEOMETRY(MULTILINESTRING, 4326) NOT NULL,
  name TEXT,
  start_date TIMESTAMP,
  end_date TIMESTAMP,
  version INT NOT NULL DEFAULT 1,
  changeset_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT constraint_fk_changeset_id
    FOREIGN KEY (changeset_id)
    REFERENCES changeset (changeset_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

--DROP TABLE IF EXISTS version_layer_1003 CASCADE ;
DROP TABLE IF EXISTS version_layer_1003 CASCADE ;
CREATE TABLE IF NOT EXISTS version_layer_1003 (
  id SERIAL,
  geom GEOMETRY(MULTILINESTRING, 4326) NOT NULL,
  name TEXT,
  start_date TIMESTAMP,
  end_date TIMESTAMP,
  version INT NOT NULL DEFAULT 1,
  changeset_id INT NOT NULL,
  is_removed BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (id, version),
  CONSTRAINT constraint_fk_changeset_id
    FOREIGN KEY (changeset_id)
    REFERENCES changeset (changeset_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- add temporal metadata
INSERT INTO temporal_columns (f_table_name, start_date_column_name, end_date_column_name, start_date, end_date, start_date_mask_id, end_date_mask_id) VALUES
('layer_1003', 'start_date', 'end_date', '1920-01-01', '1930-12-31', 1001, 1001);

-- add users in layers
INSERT INTO user_layer (layer_id, user_id, created_at, is_the_creator) VALUES (1003, 1003, '2017-04-10', TRUE);
INSERT INTO user_layer (layer_id, user_id, created_at) VALUES (1003, 1001, '2017-04-11');
INSERT INTO user_layer (layer_id, user_id, created_at) VALUES (1003, 1006, '2017-04-11');
INSERT INTO user_layer (layer_id, user_id, created_at) VALUES (1003, 1007, '2017-04-11');

-- users that follow the layer
INSERT INTO layer_followers (layer_id, user_id, created_at) VALUES (1003, 1003, '2017-01-02');
INSERT INTO layer_followers (layer_id, user_id, created_at) VALUES (1003, 1006, '2017-01-02');
INSERT INTO layer_followers (layer_id, user_id, created_at) VALUES (1003, 1007, '2017-01-02');

-- create a changeset
INSERT INTO changeset (changeset_id, created_at, layer_id, user_id_creator) VALUES (1003, '2017-04-12', 1003, 1005);

-- insert the data into the layer
INSERT INTO layer_1003 (id, geom, name, start_date, end_date, changeset_id) VALUES
(1001, ST_GeomFromText('MULTILINESTRING((-46.6237603488114 -23.5533938154249,-46.6235408108831 -23.5522660084575,-46.6233933273529 -23.5516456142714,-46.623209681096 -23.5507601376416,-46.622973981047 -23.5496552515087,-46.6236497790913 -23.5484119132552))', 4326),
'rua boa vista', '1930-01-01', '1940-12-31', 1003);
INSERT INTO layer_1003 (id, geom, name, start_date, end_date, changeset_id) VALUES
(1002, ST_GeomFromText('MULTILINESTRING((-46.6353540826681 -23.5450950669741,-46.63471434053 -23.5454695514008,-46.6343109517528 -23.5458044203441))', 4326),
 'rua tres de dezembro', '1920-01-01', '1930-12-31', 1003);
-- add data as GeoJSON
INSERT INTO layer_1003 (id, geom, start_date, end_date, changeset_id)
VALUES (1003,
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiLineString",
		    "coordinates":[[[-46.6289810574309, -23.542735394758], [-46.6267724837701, -23.5427585091922]]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	),
	'1930-01-01', '1930-12-31', 1003);

-- close the changeset
UPDATE changeset SET closed_at='2017-04-12', description='Creating layer_1003' WHERE changeset_id=1003;

-- create a open changeset
INSERT INTO changeset (changeset_id, description, created_at, layer_id, user_id_creator) VALUES (1013, 'Creating an open changeset', '2017-04-13', 1003, 1005);

-- check if the layer has features and check if the changeset was created
/*
SELECT * FROM layer_1003;
SELECT * FROM version_layer_1003;
SELECT * FROM changeset WHERE id=1003;
*/



-- add layer_1004
INSERT INTO layer (layer_id, f_table_name, name, description, source_description, created_at) VALUES
(1004, 'layer_1004', 'Streets in 1920', 'streets', '', '2017-06-15');

-- add reference
-- ...

-- add the keywords in layer
INSERT INTO layer_keyword (layer_id, keyword_id) VALUES (1004, 1040);

-- create a feature table to save the data
--DROP TABLE IF EXISTS layer_1004 CASCADE ;
DROP TABLE IF EXISTS layer_1004 CASCADE ;
CREATE TABLE IF NOT EXISTS layer_1004 (
  id SERIAL,
  geom GEOMETRY(MULTILINESTRING, 4326) NOT NULL,
  name TEXT,
  start_date TEXT,
  end_date TEXT,
  version INT NOT NULL DEFAULT 1,
  changeset_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT constraint_fk_changeset_id
    FOREIGN KEY (changeset_id)
    REFERENCES changeset (changeset_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

--DROP TABLE IF EXISTS version_layer_1004 CASCADE ;
DROP TABLE IF EXISTS version_layer_1004 CASCADE ;
CREATE TABLE IF NOT EXISTS version_layer_1004 (
  id SERIAL,
  geom GEOMETRY(MULTILINESTRING, 4326) NOT NULL,
  name TEXT,
  start_date TEXT,
  end_date TEXT,
  version INT NOT NULL DEFAULT 1,
  changeset_id INT NOT NULL,
  PRIMARY KEY (id, version),
  is_removed BOOLEAN NOT NULL DEFAULT FALSE,
  CONSTRAINT constraint_fk_changeset_id
    FOREIGN KEY (changeset_id)
    REFERENCES changeset (changeset_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- add temporal metadata
INSERT INTO temporal_columns (f_table_name, start_date_column_name, end_date_column_name, start_date, end_date, start_date_mask_id, end_date_mask_id) VALUES
('layer_1004', 'start_date', 'end_date', '1920-01-01', '1920-12-31', 1002, 1002);

-- add users in layers
INSERT INTO user_layer (layer_id, user_id, created_at, is_the_creator) VALUES (1004, 1003, '2017-06-15', TRUE);
INSERT INTO user_layer (layer_id, user_id, created_at) VALUES (1004, 1007, '2017-06-20');
INSERT INTO user_layer (layer_id, user_id, created_at) VALUES (1004, 1008, '2017-06-27');

-- users that follow the layer
INSERT INTO layer_followers (layer_id, user_id, created_at) VALUES (1004, 1003, '2017-01-09');

-- create a changeset
INSERT INTO changeset (changeset_id, created_at, layer_id, user_id_creator) VALUES (1004, '2017-06-28', 1004, 1005);

-- insert the data into the layer
INSERT INTO layer_1004 (id, geom, name, start_date, end_date, changeset_id) VALUES
(1001, ST_GeomFromText('MULTILINESTRING((-46.6223558499333 -23.5443575867494,-46.6223480680011 -23.5444468399204,-46.6218546998225 -23.545979136579))', 4326),
'rua joao briccola', '1920-01', '1920-05', 1004);
INSERT INTO layer_1004 (id, geom, name, start_date, end_date, changeset_id) VALUES
(1002, ST_GeomFromText('MULTILINESTRING((-46.6387972549339 -23.5460415609173,-46.6405962944433 -23.544623903425,-46.6417670426616 -23.5436951087793))', 4326),
'ladeira porto geral', '1920-03', '1920-04', 1004);
INSERT INTO layer_1004 (id, geom, name, start_date, end_date, changeset_id) VALUES
(1003, ST_GeomFromText('MULTILINESTRING((-46.6369959853997 -23.549500474191,-46.6367956743584 -23.5489343848123))', 4326),
'travessa porto geral', '1920-01', '1920-12', 1004);
-- add data as GeoJSON
INSERT INTO layer_1004 (id, geom, start_date, end_date, changeset_id)
VALUES (1004,
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiLineString",
		    "coordinates":[[[-46.6489360910738, -23.5471391154918], [-46.6479270334404, -23.5471656463165]]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	),
	'1920-01', '1920-12', 1004);

-- close the changeset
UPDATE changeset SET closed_at='2017-06-28', description='Creating layer_1004' WHERE changeset_id=1004;

-- check if the layer has features and check if the changeset was created
/*
SELECT * FROM layer_1004;
SELECT * FROM version_layer_1004;
SELECT * FROM changeset WHERE id=1004;
*/



-- add layer_1005
INSERT INTO layer (layer_id, f_table_name, name, description, created_at) VALUES
(1005, 'layer_1005', 'Hospitals between 1800 to 1950', 'some hospitals', '2017-08-04');

-- add reference
-- ...

-- add the keywords in layer
INSERT INTO layer_keyword (layer_id, keyword_id) VALUES (1005, 1023);

-- create a feature table to save the data
--DROP TABLE IF EXISTS layer_1005 CASCADE ;
DROP TABLE IF EXISTS layer_1005 CASCADE ;
CREATE TABLE IF NOT EXISTS layer_1005 (
  id SERIAL,
  geom GEOMETRY(MULTIPOLYGON, 4326) NOT NULL,
  name TEXT,
  start_date TEXT,
  end_date TEXT,
  version INT NOT NULL DEFAULT 1,
  changeset_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT constraint_fk_changeset_id
    FOREIGN KEY (changeset_id)
    REFERENCES changeset (changeset_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

--DROP TABLE IF EXISTS version_layer_1005 CASCADE ;
DROP TABLE IF EXISTS version_layer_1005 CASCADE ;
CREATE TABLE IF NOT EXISTS version_layer_1005 (
  id SERIAL,
  geom GEOMETRY(MULTIPOLYGON, 4326) NOT NULL,
  name TEXT,
  start_date TEXT,
  end_date TEXT,
  version INT NOT NULL DEFAULT 1,
  changeset_id INT NOT NULL,
  is_removed BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (id, version),
  CONSTRAINT constraint_fk_changeset_id
    FOREIGN KEY (changeset_id)
    REFERENCES changeset (changeset_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- add temporal metadata
INSERT INTO temporal_columns (f_table_name, start_date_column_name, end_date_column_name, start_date, end_date, start_date_mask_id, end_date_mask_id) VALUES
('layer_1005', 'start_date', 'end_date', '1920-01-01', '1940-12-31', 1002, 1002);

-- add users in layers
INSERT INTO user_layer (layer_id, user_id, created_at, is_the_creator) VALUES (1005, 1007, '2017-08-04', TRUE);

-- users that follow the layer
INSERT INTO layer_followers (layer_id, user_id, created_at) VALUES (1005, 1003, '2017-01-02');
INSERT INTO layer_followers (layer_id, user_id, created_at) VALUES (1005, 1004, '2017-01-02');
INSERT INTO layer_followers (layer_id, user_id, created_at) VALUES (1005, 1005, '2017-01-02');

-- create a changeset
INSERT INTO changeset (changeset_id, created_at, layer_id, user_id_creator) VALUES (1005, '2017-08-05', 1005, 1007);

-- insert the data into the layer
INSERT INTO layer_1005 (id, geom, name, start_date, end_date, changeset_id) VALUES (1001, ST_GeomFromText('MULTIPOLYGON(((-46.6536941024203 -23.5446440934747, -46.6536987312376 -23.5446514885665, -46.6531421851224 -23.5427759121502, -46.6531368207044 -23.5426136385048, -46.6536941024203 -23.5446440934747)))', 4326),
'Sant''Anna''s Hospital', '1920-01', '1940-12', 1005);
INSERT INTO layer_1005 (id, geom, name, start_date, end_date, changeset_id)
VALUES (1002,
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiPolygon",
		    "coordinates":[[[[-46.6531368207044, -23.5426136385048], [-46.6526581134833, -23.5401195274321], [-46.6526581134833, -23.5401195274321], [-46.6535666865397, -23.5322186250535], [-46.6531368207044, -23.5426136385048]]]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	),
	'Holy Mary''s Hospital', '1920-01', '1940-12', 1005);

-- close the changeset
UPDATE changeset SET closed_at='2017-08-05', description='Creating layer_1005' WHERE changeset_id=1005;

-- check if the layer has features and check if the changeset was created
/*
SELECT * FROM feature_layer_1005;
SELECT * FROM version_layer_1005;
SELECT * FROM changeset WHERE id=1005;
*/




-- add layer_1006
INSERT INTO layer (layer_id, f_table_name, name, description, created_at) VALUES
(1006, 'layer_1006', 'Cinemas between 1900 to 1950', '', '2017-09-04');

-- add reference
INSERT INTO reference (reference_id, description, user_id_creator) VALUES (1025,
'@Misc{frisina2017bookZ,
author = {Frisina},
title = {BookZ},
howpublished = {\url{http://www.school.com/}},
note = {Accessed on 03/04/2017},
year={2017}
}', 1007);
INSERT INTO layer_reference (layer_id, reference_id) VALUES (1006, 1025);

-- add the keywords in layer
INSERT INTO layer_keyword (layer_id, keyword_id) VALUES (1006, 1031);

-- create a feature table to save the data
--DROP TABLE IF EXISTS layer_1006 CASCADE ;
DROP TABLE IF EXISTS layer_1006 CASCADE ;
CREATE TABLE IF NOT EXISTS layer_1006 (
  id SERIAL,
  geom GEOMETRY(MULTIPOLYGON, 4326) NOT NULL,
  name TEXT,
  start_date INT,
  end_date INT,
  version INT NOT NULL DEFAULT 1,
  changeset_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT constraint_fk_changeset_id
    FOREIGN KEY (changeset_id)
    REFERENCES changeset (changeset_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

--DROP TABLE IF EXISTS version_layer_1006 CASCADE ;
DROP TABLE IF EXISTS version_layer_1006 CASCADE ;
CREATE TABLE IF NOT EXISTS version_layer_1006 (
  id SERIAL,
  geom GEOMETRY(MULTIPOLYGON, 4326) NOT NULL,
  name TEXT,
  start_date INT,
  end_date INT,
  version INT NOT NULL DEFAULT 1,
  changeset_id INT NOT NULL,
  PRIMARY KEY (id, version),
  is_removed BOOLEAN NOT NULL DEFAULT FALSE,
  CONSTRAINT constraint_fk_changeset_id
    FOREIGN KEY (changeset_id)
    REFERENCES changeset (changeset_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- add temporal metadata
INSERT INTO temporal_columns (f_table_name, start_date_column_name, end_date_column_name, start_date, end_date, start_date_mask_id, end_date_mask_id) VALUES
('layer_1006', 'start_date', 'end_date', '1900-01-01', '1930-12-31', 1003, 1003);

-- add users in layers
INSERT INTO user_layer (layer_id, user_id, created_at, is_the_creator) VALUES (1006, 1007, '2017-09-04', TRUE);
INSERT INTO user_layer (layer_id, user_id, created_at) VALUES (1006, 1008, '2017-09-10');

-- create a changeset
INSERT INTO changeset (changeset_id, created_at, layer_id, user_id_creator) VALUES (1006, '2017-09-04', 1006, 1007);

-- insert the data into the layer
INSERT INTO layer_1006 (id, geom, name, start_date, end_date, changeset_id) VALUES (1001, ST_GeomFromText('MULTIPOLYGON(((-46.6488116440144 -23.5426404452948, -46.6531396058257 -23.5465662154437, -46.6517036612052 -23.5456926854228, -46.6442476807888 -23.5477173437452, -46.6488116440144 -23.5426404452948)))', 4326),
'Cinema Roger', 1910, 1930, 1006);
-- add area as GeoJSON
INSERT INTO layer_1006 (id, geom, name, start_date, end_date, changeset_id)
VALUES (1002,
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiPolygon",
		    "coordinates":[[[[-46.6323318652266, -23.5316246866608], [-46.6316800884359, -23.5296637586354], [-46.6221419360542, -23.5384048923064], [-46.6375790530164, -23.5290461960682], [-46.6323318652266, -23.5316246866608]]]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	),
	'Joar''s cinema', 1900, 1940, 1006);

-- close the changeset
UPDATE changeset SET closed_at='2017-09-04', description='Creating layer_1006' WHERE changeset_id=1006;

-- check if the layer has features and check if the changeset was created
/*
SELECT * FROM feature_layer_1006;
SELECT * FROM version_layer_1006;
SELECT * FROM changeset WHERE id=1006;
*/



-- -----------------------------------------------------
-- Table notification
-- -----------------------------------------------------
-- clean notification table
DELETE FROM notification;

-- add notification
-- general
INSERT INTO notification (notification_id, description, created_at, user_id_creator, layer_id, keyword_id, notification_id_parent) VALUES
(1001, 'Congresso X acontecerá em 2018/03/25', '2017-01-01', 1001, NULL, NULL, NULL);
INSERT INTO notification (notification_id, description, created_at, user_id_creator, layer_id, keyword_id, notification_id_parent) VALUES
(1005, 'Evento Y no dia 24/06/2018', '2017-02-01', 1002, NULL, NULL, NULL);
	INSERT INTO notification (notification_id, description, created_at, user_id_creator, layer_id, keyword_id, notification_id_parent) VALUES
	(1006, 'Muito bom', '2017-02-01', 1003, NULL, NULL, 1005);
-- layer
INSERT INTO notification (notification_id, description, is_denunciation, created_at, user_id_creator, layer_id, keyword_id, notification_id_parent) VALUES
(1010, 'A camada contêm dados inapropriados.', TRUE, '2017-03-01', 1005, 1004, NULL, NULL);
	-- reply
	INSERT INTO notification (notification_id, description, created_at, user_id_creator, layer_id, keyword_id, notification_id_parent) VALUES
	(1011, 'Obrigado pelo aviso.', '2017-03-01', 1003, NULL, NULL, 1010);
	INSERT INTO notification (notification_id, description, created_at, user_id_creator, layer_id, keyword_id, notification_id_parent) VALUES
	(1012, 'Ações estão sendo tomadas.', '2017-03-01', 1001, NULL, NULL, 1010);
INSERT INTO notification (notification_id, description, created_at, user_id_creator, layer_id, keyword_id, notification_id_parent) VALUES
(1015, 'Muito boa camada. Parabéns.', '2017-04-05', 1002, 1002, NULL, NULL);
-- keyword
INSERT INTO notification (notification_id, description, created_at, user_id_creator, layer_id, keyword_id, notification_id_parent) VALUES
(1020, 'Uma keyword genérica', '2017-01-01', 1001, NULL, 1001, NULL);



----------------------------------------------------------------------------------------------------


/*
SELECT jsonb_build_object(
	'type', 'FeatureCollection',
	'features',   jsonb_agg(jsonb_build_object(
		'type',        'FeatureTable',
		'properties',   dict,
		'f_table_name', f_table_name,
		'geometry',  json_build_object(
			'type',      type,
			'crs',  json_build_object(
				'type',      'name',
				'properties', json_build_object('name', 'EPSG:' || srid)
			)
		)
	))
) AS row_to_json
FROM
(
	-- (2) do a JOIN with geometry_columns to get the SRID of the feature table
	SELECT isc.table_name as f_table_name, gc.srid as srid, gc.type as type, isc.dict as dict
	FROM (
		-- (1) get the columns name of the feature table as JSON
		SELECT table_name, JSON_OBJECT(ARRAY_AGG(column_name::TEXT), ARRAY_AGG(udt_name::regtype::TEXT)) as dict
		FROM information_schema.columns
		WHERE table_schema = 'public' AND unaccent(LOWER(table_name)) LIKE '%' || unaccent(LOWER('layer_1003')) || '%' AND unaccent(LOWER(table_name)) NOT LIKE '%version%'
		GROUP BY table_name
	) isc
	INNER JOIN geometry_columns gc
	ON gc.f_table_name = isc.table_name
	ORDER BY isc.table_name
) AS feature_table




SELECT *
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = 'layer_1003'
ORDER BY ordinal_position

*/

/*
select * from layer_1006;

INSERT INTO layer_1006 (id, geom, name, start_date, end_date, changeset_id)
VALUES (1005, ST_SetSRID(
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiPolygon",
		    "coordinates":[[[[-46.6323318652266, -23.5316246866608], [-46.6316800884359, -23.5296637586354], [-46.6221419360542, -23.5384048923064], [-46.6375790530164, -23.5290461960682], [-46.6323318652266, -23.5316246866608]]]]
		}'
	), 4326),
	'Joar''s cinema', 1900, 1940, 1006);

SELECT srid FROM geometry_columns WHERE f_table_name='layer_1001';
*/
/*
INSERT INTO layer_1002 (start_date, changeset_id, address, end_date, geom)
VALUES ('1870-01-01', 1, 'R. São José', '1870-12-31', ST_SetSRID(ST_GeomFromGeoJSON('{"type": "MultiPoint", "coordinates": [[-46.6375790530164, -23.5290461960682]]}'), 4326))
RETURNING id;


SELECT *
FROM
(
	-- notifications that a user follows
	SELECT notification_id, description, created_at, is_denunciation, user_id_creator, layer_id, keyword_id, notification_id_parent FROM
	(SELECT layer_id AS lf_layer_id FROM layer_followers WHERE user_id = 1006) lf INNER JOIN notification n
	ON lf.lf_layer_id = n.layer_id
		-- union the tables
		UNION
	-- general notifications
	SELECT * FROM notification WHERE layer_id is NULL AND keyword_id is NULL AND notification_id_parent is NULL
) __notification__
WHERE is_denunciation = FALSE
ORDER BY created_at DESC, notification_id
*/

/*
SELECT  ST_Transform(
	    ST_MakeEnvelope (
		313389.67, 7343788.61,
		360663.23, 7416202.05,
		29193
	    )
	, 4326);

SELECT ST_Union(geom) as geom FROM streets_pilot_area;




SELECT ST_Contains(bb_default_city.geom, union_f_table.geom)
FROM
(
	-- get the union of a feature table
	SELECT ST_Transform(ST_Union(geom), 4326) as geom FROM streets_pilot_area
) union_f_table,
(
	-- create a bouding box of the default city (by default is SP city)
	SELECT  ST_Transform(
	    ST_MakeEnvelope (
		313389.67, 7343788.61,
		360663.23, 7416202.05,
		29193
	    )
	, 4326) as geom
) bb_default_city;


*/

