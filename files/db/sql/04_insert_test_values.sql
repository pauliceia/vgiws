
--DROP TABLE IF EXISTS new_layer CASCADE ;
--DROP TABLE IF EXISTS version_new_layer CASCADE ;
--DROP TABLE IF EXISTS points CASCADE ;



-- -----------------------------------------------------
-- Table pauliceia_user
-- -----------------------------------------------------
-- clean user table
DELETE FROM pauliceia_user;

-- add users
-- PS: the passwords are in sha512 hash

--login_date, is_the_admin, can_add_layer, receive_notification_by_email) 
-- password - admin
INSERT INTO pauliceia_user (user_id, username, email, password, name, created_at, is_email_valid, terms_agreed, login_date, is_the_admin, can_add_layer, receive_notification_by_email) 
VALUES (1001, 'admin', 'admin@admin.com', 'c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec', 
'Administrator', '2017-01-01', TRUE, TRUE, '2017-01-01', TRUE, TRUE, FALSE);

-- password - rodrigo
INSERT INTO pauliceia_user (user_id, username, email, password, name, created_at, is_email_valid, terms_agreed, login_date, is_the_admin, can_add_layer, receive_notification_by_email) 
VALUES (1002, 'rodrigo', 'rodrigo@admin.com', '3ad7e557497e106756c44b7f3f401fd3f28f84c3c9ad989157868d03686f683f82d5cde1a096c4bbdbd76287e96e9a04d9f0ce8726b945c95f01b18361088a0d', 
'Rodrigo', '2017-03-03', TRUE, TRUE, '2017-03-03', TRUE, TRUE, FALSE);

-- password - miguel
INSERT INTO pauliceia_user (user_id, username, email, password, name, created_at, is_email_valid, terms_agreed, login_date, is_the_admin, can_add_layer, receive_notification_by_email) 
VALUES (1003, 'miguel', 'miguel@admin.com', 'e1fc7a4313def98ae5303b0448c89d9a5126f3239608950859f3ea6fdeb8b19f6f7c103ecf97700be851cfbf8cda756c0929498021c675c643809eeeb4ebcbda', 
'Miguel', '2017-05-08', FALSE, TRUE, '2017-05-08', TRUE, TRUE, FALSE);

-- password - rafael
INSERT INTO pauliceia_user (user_id, username, email, password, name, created_at, is_email_valid, terms_agreed, login_date, is_the_admin, can_add_layer, receive_notification_by_email) 
VALUES (1004, 'rafael', 'rafael@admin.com', 'c5663337df01fe3ab80478e78963534956a7e5446d72b16db9f33a36c787954414fea6de37a02d5f32ac2fe18f010068688d707e6dd260ca1f0a255f6d2f1959', 
'Rafael', '2017-06-09', TRUE, FALSE, '2017-06-09', FALSE, TRUE, TRUE);

-- password - gabriel
INSERT INTO pauliceia_user (user_id, username, email, password, name, created_at, is_email_valid, terms_agreed, login_date, is_the_admin, can_add_layer, receive_notification_by_email) 
VALUES (1005, 'gabriel', 'gabriel@admin.com', '5dbe7d079067809bb06f7c80de78ecb9d914f5735265148cd704f85353fc0b5114ebbfc960539cd3f430e7b12eb3fdc261726bb756bab9658c6db6a302913df1', 
'Gabriel', '2017-09-20', FALSE, FALSE, '2017-09-20', FALSE, TRUE, TRUE);

-- password - fernanda
INSERT INTO pauliceia_user (user_id, username, email, password, created_at, is_email_valid, terms_agreed, login_date, is_the_admin, can_add_layer, receive_notification_by_email) 
VALUES (1006, 'fernanda', 'fernanda@gmail.com', 'fernanda',
'2017-01-19', TRUE, FALSE, '2017-01-19', FALSE, FALSE, TRUE);

-- password - ana
INSERT INTO pauliceia_user (user_id, username, email, password, created_at, is_email_valid, terms_agreed, login_date, is_the_admin, can_add_layer, receive_notification_by_email) 
VALUES (1007, 'ana', 'ana@gmail.com', 'ana',
'2017-01-18', FALSE, TRUE, '2017-01-18', FALSE, FALSE, FALSE);

-- password - bea
INSERT INTO pauliceia_user (user_id, username, email, password, created_at, is_email_valid, terms_agreed, login_date, is_the_admin, can_add_layer, receive_notification_by_email) 
VALUES (1008, 'bea', 'bea@gmail.com', 'bea', 
'2017-01-30', FALSE, FALSE, '2017-01-30', FALSE, FALSE, FALSE);


-- SELECT * FROM user_;


/*
-- -----------------------------------------------------
-- Table auth
-- -----------------------------------------------------
-- clean auth table
DELETE FROM auth;

-- insert values in auth table
-- user 1001
INSERT INTO auth (id, is_admin, is_manager, is_curator, fk_user_id) VALUES (1001, TRUE, TRUE, TRUE, 1001);
-- user 1002
INSERT INTO auth (id, is_admin, is_manager, is_curator, fk_user_id) VALUES (1002, TRUE, TRUE, TRUE, 1002);
-- user 1003
INSERT INTO auth (id, is_admin, is_manager, is_curator, fk_user_id) VALUES (1003, FALSE, TRUE, TRUE, 1003);
-- user 1004
INSERT INTO auth (id, is_admin, is_manager, is_curator, fk_user_id) VALUES (1004, FALSE, FALSE, TRUE, 1004);
-- user 1005
INSERT INTO auth (id, is_admin, is_manager, is_curator, fk_user_id) VALUES (1005, FALSE, FALSE, TRUE, 1005);
-- user 1006
INSERT INTO auth (id, is_admin, is_manager, is_curator, fk_user_id) VALUES (1006, FALSE, FALSE, TRUE, 1006);
-- user 1007
INSERT INTO auth (id, is_admin, is_manager, is_curator, fk_user_id) VALUES (1007, FALSE, FALSE, FALSE, 1007);
-- user 1008
INSERT INTO auth (id, is_admin, is_manager, is_curator, fk_user_id) VALUES (1008, FALSE, FALSE, FALSE, 1008);

*/



-- -----------------------------------------------------
-- Table keyword
-- -----------------------------------------------------
-- clean table
DELETE FROM keyword;

INSERT INTO keyword (keyword_id, name, parent_id, user_id_creator, created_at) VALUES (1001, 'generic', NULL, 1001, '2017-01-01');
    INSERT INTO keyword (keyword_id, name, parent_id, user_id_creator, created_at) VALUES (1002, 'event', 1001, 1001, '2017-01-01');
        -- event's children (1002)
        INSERT INTO keyword (keyword_id, name, parent_id, user_id_creator, created_at) VALUES (1003, 'crime', 1002, 1001, '2017-01-01');
            -- crime's children (1003)
            INSERT INTO keyword (keyword_id, name, parent_id, user_id_creator, created_at) VALUES (1004, 'assalt', 1003, 1001, '2017-01-01');
            INSERT INTO keyword (keyword_id, name, parent_id, user_id_creator, created_at) VALUES (1005, 'robbery', 1003, 1001, '2017-01-01');

        INSERT INTO keyword (keyword_id, name, parent_id, user_id_creator, created_at) VALUES (1010, 'disease', 1002, 1001, '2017-01-01');

    INSERT INTO keyword (keyword_id, name, parent_id, user_id_creator, created_at) VALUES (1020, 'object', 1001, 1001, '2017-01-01');
        -- object's children (1020)
        INSERT INTO keyword (keyword_id, name, parent_id, user_id_creator, created_at) VALUES (1021, 'building', 1020, 1001, '2017-01-01');
            -- building's children (1021)
            INSERT INTO keyword (keyword_id, name, parent_id, user_id_creator, created_at) VALUES (1022, 'school', 1021, 1001, '2017-01-01');
            INSERT INTO keyword (keyword_id, name, parent_id, user_id_creator, created_at) VALUES (1023, 'hospital', 1021, 1001, '2017-01-01');

        INSERT INTO keyword (keyword_id, name, parent_id, user_id_creator, created_at) VALUES (1030, 'cultural place', 1020, 1001, '2017-01-01');
            -- cultural place's children (1030)
            INSERT INTO keyword (keyword_id, name, parent_id, user_id_creator, created_at) VALUES (1031, 'cinema', 1030, 1001, '2017-01-01');

        INSERT INTO keyword (keyword_id, name, parent_id, user_id_creator, created_at) VALUES (1040, 'street', 1020, 1001, '2017-01-01');

        INSERT INTO keyword (keyword_id, name, parent_id, user_id_creator, created_at) VALUES (1041, 'address', 1020, 1001, '2017-01-01');



-- -----------------------------------------------------
-- Table curator
-- -----------------------------------------------------
-- clean table
DELETE FROM curator;

INSERT INTO curator (user_id, keyword_id, region, created_at) VALUES (1001, 1001, '', '2018-01-01');
INSERT INTO curator (user_id, keyword_id, region, created_at) VALUES (1002, 1002, '', '2018-01-10');
INSERT INTO curator (user_id, keyword_id, region, created_at) VALUES (1003, 1020, '', '2018-01-15');
INSERT INTO curator (user_id, keyword_id, region, created_at) VALUES (1004, 1003, '', '2018-02-20');
INSERT INTO curator (user_id, keyword_id, region, created_at) VALUES (1005, 1010, '', '2018-02-22');
INSERT INTO curator (user_id, keyword_id, region, created_at) VALUES (1006, 1021, '', '2018-03-24');



-- -----------------------------------------------------
-- Table layer_keyword
-- -----------------------------------------------------
-- clean table
DELETE FROM layer_keyword;
            
            

/*
-- -----------------------------------------------------
-- Table changeset
-- -----------------------------------------------------
-- clean changeset table
DELETE FROM changeset;


-- add changeset open
-- closed changesets (they will be closed in the final of file)
INSERT INTO changeset (id, description, created_at, fk_layer_id, fk_user_id) VALUES (1001, 'a changeset created', '2017-10-20', 1001, 1001);
INSERT INTO changeset (id, description, created_at, fk_layer_id, fk_user_id) VALUES (1002, 'changeset test', '2017-11-10', 1002, 1002);
INSERT INTO changeset (id, description, created_at, fk_layer_id, fk_user_id) VALUES (1003, 'a changeset created', '2017-11-15', 1001, 1001);
INSERT INTO changeset (id, description, created_at, fk_layer_id, fk_user_id) VALUES (1004, 'changeset test', '2017-01-20', 1002, 1002);
-- open changesets
INSERT INTO changeset (id, created_at, fk_layer_id, fk_user_id) VALUES (1005, '2017-03-25', 1003, 1003);
INSERT INTO changeset (id, created_at, fk_layer_id, fk_user_id) VALUES (1006, '2017-05-13', 1004, 1004);
*/


-- -----------------------------------------------------
-- Table reference
-- -----------------------------------------------------
-- clean table
DELETE FROM reference;


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
-- Table layer
-- -----------------------------------------------------
-- clean table
DELETE FROM layer;


-- add layer 1001
INSERT INTO layer (layer_id, f_table_name, name, description, source_description, created_at, is_published, user_id_published_by) VALUES 
(1001, 'layer_1001', 'Addresses in 1869', '', '', '2017-01-01', TRUE, 1001);

-- add reference
INSERT INTO reference (reference_id, bibtex) VALUES (1001, 
'@Misc{jorge2017book1,
author = {Jorge},
title = {Book1},
howpublished = {\url{http://www.link.org/}},
note = {Accessed on 01/01/2017},
year={2017}
}');
INSERT INTO layer_reference (layer_id, reference_id) VALUES (1001, 1001);

INSERT INTO reference (reference_id, bibtex) VALUES (1002, 
'@Misc{ana2017article2,
author = {Ana},
title = {Article2},
howpublished = {\url{http://www.myhost.org/}},
note = {Accessed on 05/02/2017},
year={2017}
}');
INSERT INTO layer_reference (layer_id, reference_id) VALUES (1001, 1002);

-- add the keywords in layer
INSERT INTO layer_keyword (layer_id, keyword_id) VALUES (1001, 1041);

-- create a feature table to save the data
DROP TABLE IF EXISTS layer_1001 CASCADE ;
CREATE TABLE IF NOT EXISTS layer_1001 (
  id SERIAL,
  geom GEOMETRY(MULTIPOINT, 4326) NOT NULL,
  address TEXT,
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

DROP TABLE IF EXISTS version_layer_1001 CASCADE ;
CREATE TABLE IF NOT EXISTS version_layer_1001 (
  id SERIAL,
  geom GEOMETRY(MULTIPOINT, 4326) NOT NULL,
  address TEXT,
  start_date TEXT,
  end_date TEXT,
  version INT NOT NULL DEFAULT 1,
  changeset_id INT NOT NULL,
  PRIMARY KEY (id, version),
  CONSTRAINT constraint_fk_changeset_id
    FOREIGN KEY (changeset_id)
    REFERENCES changeset (changeset_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- add users in layers (the main user is added when the layer is created)
INSERT INTO user_layer (layer_id, user_id, created_at, is_the_creator) VALUES (1001, 1001, '2017-01-02', TRUE);
INSERT INTO user_layer (layer_id, user_id, created_at, is_the_creator) VALUES (1001, 1002, '2017-01-03', FALSE);

-- create a changeset
INSERT INTO changeset (changeset_id, created_at, layer_id, user_id) VALUES (1001, '2017-01-05', 1001, 1001);

-- insert the data into the layer
INSERT INTO layer_1001 (id, geom, address, start_date, end_date, changeset_id) VALUES 
(1001, ST_GeomFromText('MULTIPOINT((-23.546421 -46.635722))', 4326), 'R. São José', '1869', '1869', 1001);
INSERT INTO layer_1001 (id, geom, address, start_date, end_date, changeset_id) VALUES 
(1002, ST_GeomFromText('MULTIPOINT((-23.55045 -46.634272))', 4326), 'R. Marechal Deodoro', '1869', '1869', 1001);
-- add data as GeoJSON
INSERT INTO layer_1001 (id, geom, changeset_id) 
VALUES (1003, 
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiPoint",
		    "coordinates":[[-54, 33]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	), 
	1001);

-- close the changeset
UPDATE changeset SET description='adding some addresses', closed_at='2017-01-05' WHERE changeset_id=1001;

-- create a open changeset
INSERT INTO changeset (changeset_id, created_at, layer_id, user_id) VALUES (1011, '2017-01-08', 1001, 1001);

-- verify if the layer has features and verify if the changeset was created
/*
SELECT * FROM layer_1001;
SELECT * FROM version_layer_1001;
SELECT * FROM changeset WHERE id=1001;
*/



-- add layer 1002
INSERT INTO layer (layer_id, f_table_name, name, description, source_description, created_at, is_published, user_id_published_by) VALUES 
(1002, 'layer_1002', 'Robberies between 1880 to 1900', '', '', '2017-03-05', TRUE, 1003);

-- add reference
INSERT INTO reference (reference_id, bibtex) VALUES (1005, 
'@Misc{marco2017articleB,
author = {Marco},
title = {ArticleB},
howpublished = {\url{http://www.link_to_document.org/}},
note = {Accessed on 02/02/2017},
year={2017}
}');
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

--DROP TABLE IF EXISTS version_layer_1002 CASCADE ;
DROP TABLE IF EXISTS version_layer_1002 CASCADE ;
CREATE TABLE IF NOT EXISTS version_layer_1002 (
  id SERIAL,
  geom GEOMETRY(MULTIPOINT, 4326) NOT NULL,
  address TEXT,
  start_date TEXT,
  end_date TEXT,
  version INT NOT NULL DEFAULT 1,
  changeset_id INT NOT NULL,
  PRIMARY KEY (id, version),
  CONSTRAINT constraint_fk_changeset_id
    FOREIGN KEY (changeset_id)
    REFERENCES changeset (changeset_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- add users in layers (the main user is added when the layer is created)
INSERT INTO user_layer (layer_id, user_id, created_at, is_the_creator) VALUES (1002, 1003, '2017-03-05', TRUE);
INSERT INTO user_layer (layer_id, user_id, created_at, is_the_creator) VALUES (1002, 1004, '2017-03-05', FALSE);

-- create a changeset
INSERT INTO changeset (changeset_id, created_at, layer_id, user_id) VALUES (1002, '2017-03-05', 1002, 1003);

-- insert the data into the layer
INSERT INTO layer_1002 (id, geom, address, start_date, end_date, changeset_id) VALUES 
(1006, ST_GeomFromText('MULTIPOINT((-23.542626 -46.638684))', 4326), 'R. 11 de Junho, 9 = D. José de Barros', '1886', '', 1002);
INSERT INTO layer_1002 (id, geom, address, start_date, end_date, changeset_id) VALUES 
(1007, ST_GeomFromText('MULTIPOINT((-23.542626 -46.638684))', 4326), 'R. 15 de Novembro, 17A', '1890', '', 1002);
INSERT INTO layer_1002 (id, geom, address, start_date, end_date, changeset_id) VALUES 
(1008, ST_GeomFromText('MULTIPOINT((-23.530159 -46.654885))', 4326), 'R. Barra Funda, 74', '1897', '', 1002);
-- add data as GeoJSON
INSERT INTO layer_1002 (id, geom, changeset_id) 
VALUES (1009, 
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiPoint",
		    "coordinates":[[-21, 42]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	), 
	1002);

-- close the changeset
UPDATE changeset SET description='adding robberies', closed_at='2017-03-05' WHERE changeset_id=1002;

-- verify if the layer has features and verify if the changeset was created
/*
SELECT * FROM layer_1002;
SELECT * FROM version_layer_1002;
SELECT * FROM changeset WHERE id=1002;
*/



-- add layer_1003
INSERT INTO layer (layer_id, f_table_name, name, description, source_description, created_at) VALUES 
(1003, 'layer_1003', 'Streets in 1930', '', '', '2017-04-10');

-- add reference
INSERT INTO reference (reference_id, bibtex) VALUES (1010, 
'@Misc{marco2017articleB,
author = {Marco},
title = {ArticleB},
howpublished = {\url{http://www.link_to_document.org/}},
note = {Accessed on 02/02/2017},
year={2017}
}');
INSERT INTO layer_reference (layer_id, reference_id) VALUES (1003, 1010);

-- add the keywords in layer
INSERT INTO layer_keyword (layer_id, keyword_id) VALUES (1003, 1040);

-- create a feature table to save the data
--DROP TABLE IF EXISTS layer_1003 CASCADE ;
DROP TABLE IF EXISTS layer_1003 CASCADE ;
CREATE TABLE IF NOT EXISTS layer_1003 (
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

--DROP TABLE IF EXISTS version_layer_1003 CASCADE ;
DROP TABLE IF EXISTS version_layer_1003 CASCADE ;
CREATE TABLE IF NOT EXISTS version_layer_1003 (
  id SERIAL,
  geom GEOMETRY(MULTILINESTRING, 4326) NOT NULL,
  name TEXT,
  start_date TEXT,
  end_date TEXT,
  version INT NOT NULL DEFAULT 1,
  changeset_id INT NOT NULL,
  PRIMARY KEY (id, version),
  CONSTRAINT constraint_fk_changeset_id
    FOREIGN KEY (changeset_id)
    REFERENCES changeset (changeset_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- add users in layers
INSERT INTO user_layer (layer_id, user_id, created_at, is_the_creator) VALUES (1003, 1005, '2017-04-10', TRUE);
INSERT INTO user_layer (layer_id, user_id, created_at, is_the_creator) VALUES (1003, 1006, '2017-04-11', FALSE);
INSERT INTO user_layer (layer_id, user_id, created_at, is_the_creator) VALUES (1003, 1007, '2017-04-11', FALSE);

-- create a changeset
INSERT INTO changeset (changeset_id, created_at, layer_id, user_id) VALUES (1003, '2017-04-12', 1003, 1005);

-- insert the data into the layer
INSERT INTO layer_1003 (id, geom, name, start_date, end_date, changeset_id) VALUES 
(1001, ST_GeomFromText('MULTILINESTRING((333188.261004703 7395284.32488995,333205.817689791 7395247.71277836,333247.996555184 7395172.56160195,333261.133400433 7395102.3470075,333270.981533908 7395034.48052247,333277.885095545 7394986.25678192))', 4326), 
'rua boa vista', '1930', '1930', 1003);
INSERT INTO layer_1003 (id, geom, name, start_date, end_date, changeset_id) VALUES 
(1002, ST_GeomFromText('MULTILINESTRING((333270.653184563 7395036.74327773,333244.47769325 7395033.35326418,333204.141105934 7395028.41654752,333182.467715735 7395026.2492085))', 4326),
 'rua tres de dezembro', '1930', '1930', 1003);
-- add data as GeoJSON
INSERT INTO layer_1003 (id, geom, changeset_id) 
VALUES (1003, 
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiLineString",
		    "coordinates":[[[-21, 56], [-32, 31], [-23, 74]]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	), 
	1003);

-- close the changeset
UPDATE changeset SET description='creating streets', closed_at='2017-04-12' WHERE changeset_id=1003;

-- create a open changeset
INSERT INTO changeset (changeset_id, created_at, layer_id, user_id) VALUES (1013, '2017-04-13', 1003, 1005);

-- verify if the layer has features and verify if the changeset was created
/*
SELECT * FROM layer_1003;
SELECT * FROM version_layer_1003;
SELECT * FROM changeset WHERE id=1003;
*/



-- add layer_1004
INSERT INTO layer (layer_id, f_table_name, name, description, source_description, created_at, is_published, user_id_published_by) VALUES 
(1004, 'layer_1004', 'Streets in 1920', 'streets', '', '2017-06-15', TRUE, 1003);

-- add reference
-- INSERT INTO reference (id, description, fk_layer_id) VALUES (1015, '', 1004);

-- add the keywords in layer
INSERT INTO layer_keyword (layer_id, keyword_id) VALUES (1004, 1040);

-- create a feature table to save the data
--DROP TABLE IF EXISTS layer_1004 CASCADE ;
DROP TABLE IF EXISTS layer_1004 CASCADE ;
CREATE TABLE IF NOT EXISTS layer_1004 (
  id SERIAL,
  geom GEOMETRY(MULTILINESTRING, 4326) NOT NULL,
  name TEXT,
  start_date TEXT NULL,
  end_date TEXT NULL,
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
  start_date TEXT NULL,
  end_date TEXT NULL,
  version INT NOT NULL DEFAULT 1,
  changeset_id INT NOT NULL,
  PRIMARY KEY (id, version),
  CONSTRAINT constraint_fk_changeset_id
    FOREIGN KEY (changeset_id)
    REFERENCES changeset (changeset_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- add users in layers
INSERT INTO user_layer (layer_id, user_id, created_at, is_the_creator) VALUES (1004, 1005, '2017-06-15', TRUE);
INSERT INTO user_layer (layer_id, user_id, created_at, is_the_creator) VALUES (1004, 1007, '2017-06-20', FALSE);
INSERT INTO user_layer (layer_id, user_id, created_at, is_the_creator) VALUES (1004, 1008, '2017-06-27', FALSE);

-- create a changeset
INSERT INTO changeset (changeset_id, created_at, layer_id, user_id) VALUES (1004, '2017-06-28', 1004, 1005);

-- insert the data into the layer
INSERT INTO layer_1004 (id, geom, name, start_date, end_date, changeset_id) VALUES 
(1001, ST_GeomFromText('MULTILINESTRING((333175.973956142 7395098.49130924,333188.494819187 7395102.10309665,333248.637266893 7395169.13708777))', 4326), 
'rua joao briccola', '1920', '1920', 1004);
INSERT INTO layer_1004 (id, geom, name, start_date, end_date, changeset_id) VALUES 
(1002, ST_GeomFromText('MULTILINESTRING((333247.996555184 7395172.56160195,333255.762310051 7395178.46616912,333307.926051785 7395235.76603312,333354.472159794 7395273.32392717))', 4326), 
'ladeira porto geral', '1920', '1920', 1004);
INSERT INTO layer_1004 (id, geom, name, start_date, end_date, changeset_id) VALUES 
(1003, ST_GeomFromText('MULTILINESTRING((333266.034554577 7395292.9053933,333308.06080675 7395235.87476644))', 4326), 
'travessa porto geral', '1920', '1920', 1004);
-- add data as GeoJSON
INSERT INTO layer_1004 (id, geom, changeset_id) 
VALUES (1004, 
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiLineString",
		    "coordinates":[[[-54, 33], [-32, 31], [-36, 89]]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	), 
	1004);

-- close the changeset
UPDATE changeset SET description='adding streets', closed_at='2017-06-28' WHERE changeset_id=1004;

-- verify if the layer has features and verify if the changeset was created
/*
SELECT * FROM layer_1004;
SELECT * FROM version_layer_1004;
SELECT * FROM changeset WHERE id=1004;
*/



-- add layer_1005
INSERT INTO layer (layer_id, f_table_name, name, description, created_at) VALUES 
(1005, 'layer_1005', 'Hospitals between 1800 to 1950', 'some hospitals', '2017-08-04');

-- add reference
--INSERT INTO reference_ (id, description, fk_layer_id) VALUES (1020, 'bookA', 1005);

-- add the keywords in layer
INSERT INTO layer_keyword (layer_id, keyword_id) VALUES (1005, 1023);

-- create a feature table to save the data
--DROP TABLE IF EXISTS layer_1005 CASCADE ;
DROP TABLE IF EXISTS layer_1005 CASCADE ;
CREATE TABLE IF NOT EXISTS layer_1005 (
  id SERIAL,
  geom GEOMETRY(MULTIPOLYGON, 4326) NOT NULL,
  name TEXT,
  start_date TEXT NULL,
  end_date TEXT NULL,
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
  start_date TEXT NULL,
  end_date TEXT NULL,
  version INT NOT NULL DEFAULT 1,
  changeset_id INT NOT NULL,
  PRIMARY KEY (id, version),
  CONSTRAINT constraint_fk_changeset_id
    FOREIGN KEY (changeset_id)
    REFERENCES changeset (changeset_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- add users in layers
INSERT INTO user_layer (layer_id, user_id, created_at, is_the_creator) VALUES (1005, 1007, '2017-08-04', TRUE);

-- create a changeset
INSERT INTO changeset (changeset_id, created_at, layer_id, user_id) VALUES (1005, '2017-08-05', 1005, 1007);

-- insert the data into the layer
INSERT INTO layer_1005 (id, geom, name, start_date, end_date, changeset_id) VALUES 
(1001, ST_GeomFromText('MULTIPOLYGON(((0 0, 1 1, 2 2, 3 3, 0 0)))', 4326), 'Sant''Anna''s Hospital', '1870', '1940', 1005);
INSERT INTO layer_1005 (id, geom, name, start_date, end_date, changeset_id) 
VALUES (1002, 
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiPolygon",
		    "coordinates":[[[[-12, 32], [-21, 56], [-32, 31], [-23, 74], [-12, 32]]]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	), 
	'Holy Mary''s Hospital', '1890', '1950', 1005);

-- close the changeset
UPDATE changeset SET description='adding some hospitals', closed_at='2017-08-05' WHERE changeset_id=1005;

-- verify if the layer has features and verify if the changeset was created
/*
SELECT * FROM feature_layer_1005;
SELECT * FROM version_layer_1005;
SELECT * FROM changeset WHERE id=1005;
*/




-- add layer_1006
INSERT INTO layer (layer_id, f_table_name, name, description, created_at, is_published, user_id_published_by) VALUES 
(1006, 'layer_1006', 'Cinemas between 1900 to 1950', '', '2017-09-04', TRUE, 1003);

-- add reference
INSERT INTO reference (reference_id, bibtex) VALUES (1025,
'@Misc{frisina2017bookZ,
author = {Frisina},
title = {BookZ},
howpublished = {\url{http://www.school.com/}},
note = {Accessed on 03/04/2017},
year={2017}
}');
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
  start_date TEXT NULL,
  end_date TEXT NULL,
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
  start_date TEXT NULL,
  end_date TEXT NULL,
  version INT NOT NULL DEFAULT 1,
  changeset_id INT NOT NULL,
  PRIMARY KEY (id, version),
  CONSTRAINT constraint_fk_changeset_id
    FOREIGN KEY (changeset_id)
    REFERENCES changeset (changeset_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- add users in layers
INSERT INTO user_layer (layer_id, user_id, created_at) VALUES (1006, 1007, '2017-09-04');
INSERT INTO user_layer (layer_id, user_id, created_at) VALUES (1006, 1008, '2017-09-10');

-- create a changeset
INSERT INTO changeset (changeset_id, created_at, layer_id, user_id) VALUES (1006, '2017-09-04', 1006, 1007);

-- insert the data into the layer
INSERT INTO layer_1006 (id, geom, name, start_date, end_date, changeset_id) VALUES 
(1001, ST_GeomFromText('MULTIPOLYGON(((2 2, 3 3, 4 4, 5 5, 2 2)))', 4326), 'Cinema Roger', '1910', '1930', 1006);
-- add area as GeoJSON 
INSERT INTO layer_1006 (id, geom, name, start_date, end_date, changeset_id) 
VALUES (1002, 
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiPolygon",
		    "coordinates":[[[[-54, 33], [-32, 31], [-36, 89], [-54, 33]]]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	), 
	'Joar''s cinema', '1900', '1940', 1006);

-- close the changeset
UPDATE changeset SET description='creating cinemas', closed_at='2017-09-04' WHERE changeset_id=1006;

-- verify if the layer has features and verify if the changeset was created
/*
SELECT * FROM feature_layer_1005;
SELECT * FROM version_layer_1005;
SELECT * FROM changeset WHERE id=1005;
*/












/*
-- -----------------------------------------------------
-- Table notification
-- -----------------------------------------------------
-- clean notification table
DELETE FROM notification;

-- add notification
INSERT INTO notification (id, created_at, fk_user_id, tags) VALUES (1001, '2017-01-01', 1001,
'{"body": "Happy Birthday", "url": "", "type": "birthday"}');
INSERT INTO notification (id, created_at, fk_user_id, tags) VALUES (1002, '2017-03-25', 1001,
'{"body": "You was added in a group called X", "url": "", "type": "group"}');
INSERT INTO notification (id, created_at, fk_user_id, is_read, tags) VALUES (1003, '2017-12-25', 1001, TRUE,
'{"body": "Created a new project in group X", "url": "", "type": "project"}');
INSERT INTO notification (id, created_at, fk_user_id, tags) VALUES (1004, '2017-05-13', 1002,
'{"body": "Created a new layer in project Y", "url": "", "type": "layer"}');
INSERT INTO notification (id, created_at, fk_user_id, tags) VALUES (1005, '2017-12-25', 1002,
'{"body": "A new review was made in layer Z", "url": "", "type": "review"}');
INSERT INTO notification (id, created_at, fk_user_id, tags) VALUES (1006, '2017-05-13', 1003,
'{"body": "You gained a new trophy", "url": "", "type": "award"}');
INSERT INTO notification (id, created_at, removed_at, fk_user_id, is_read, visible, tags) VALUES (1007, '2017-08-15', '2017-10-25', 1003, TRUE, FALSE,
'{"body": "Created a new project in group X", "url": "", "type": "project"}');
INSERT INTO notification (id, created_at, fk_user_id, tags) VALUES (1008, '2017-12-25', 1004,
'{"body": "You gained more points", "url": "", "type": "point"}');
INSERT INTO notification (id, created_at, removed_at, fk_user_id, visible, tags) VALUES (1009, '2017-06-24', '2017-12-25', 1005, FALSE,
'{"body": "A new review was made in layer Z", "url": "", "type": "review"}');
INSERT INTO notification (id, created_at, fk_user_id, is_read, tags) VALUES (1010, '2017-05-13', 1005, TRUE,
'{"body": "You gained more points", "url": "", "type": "point"}');
*/


/*
-- -----------------------------------------------------
-- Table current_point
-- -----------------------------------------------------
-- clean current_point table
DELETE FROM current_point;

-- add node
INSERT INTO current_point (id, geom, fk_changeset_id, tags) VALUES (1001, ST_GeomFromText('MULTIPOINT((-23.546421 -46.635722))', 4326), 1001, 
'{"address": "R. São José", "start_date": "1869", "end_date": "1869"}');
INSERT INTO current_point (id, geom, fk_changeset_id, tags) VALUES (1002, ST_GeomFromText('MULTIPOINT((-23.55045 -46.634272))', 4326), 1002,
'{"address": "R. Marechal Deodoro", "start_date": "1878", "end_date": "1910"}');
INSERT INTO current_point (id, geom, fk_changeset_id, tags) VALUES (1003, ST_GeomFromText('MULTIPOINT((-23.542626 -46.638684))', 4326), 1003,
'{"address": "R. 11 de Junho, 9 = D. José de Barros", "start_date": "1886", "end_date": "1916"}');
INSERT INTO current_point (id, geom, fk_changeset_id, tags) VALUES (1004, ST_GeomFromText('MULTIPOINT((-23.547951 -46.634215))', 4326), 1004,
'{"address": "R. 15 de Novembro, 17A", "start_date": "1890", "end_date": "1911"}');
INSERT INTO current_point (id, geom, fk_changeset_id, tags) VALUES (1005, ST_GeomFromText('MULTIPOINT((-23.530159 -46.654885))', 4326), 1001,
'{"address": "R. Barra Funda, 74", "start_date": "1897", "end_date": "1897"}');
-- add node as GeoJSON
INSERT INTO current_point (id, geom, fk_changeset_id) 
VALUES (1006, 
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiPoint",
		    "coordinates":[[-54, 33]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	), 
	1003);
INSERT INTO current_point (id, geom, fk_changeset_id) 
VALUES (1007, 
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiPoint",
		    "coordinates":[[-21, 42]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	), 
	1002);



-- -----------------------------------------------------
-- Operations with current_node
-- -----------------------------------------------------

-- "remove" some nodes
UPDATE current_point SET visible = FALSE WHERE id>=1003 AND id<=1005;



-- -----------------------------------------------------
-- Table current_line
-- -----------------------------------------------------
-- clean current_line table
DELETE FROM current_line;

-- add way
INSERT INTO current_line (id, geom, fk_changeset_id, tags) VALUES (1001, ST_GeomFromText('MULTILINESTRING((333188.261004703 7395284.32488995,333205.817689791 7395247.71277836,333247.996555184 7395172.56160195,333261.133400433 7395102.3470075,333270.981533908 7395034.48052247,333277.885095545 7394986.25678192))', 4326), 1001,
'{"name": "rua boa vista", "start_date": "1930", "end_date": "1930"}');
INSERT INTO current_line (id, geom, fk_changeset_id, tags) VALUES (1002, ST_GeomFromText('MULTILINESTRING((333270.653184563 7395036.74327773,333244.47769325 7395033.35326418,333204.141105934 7395028.41654752,333182.467715735 7395026.2492085))', 4326), 1002,
'{"name": "rua tres de dezembro", "start_date": "1930", "end_date": "1930"}');
INSERT INTO current_line (id, geom, fk_changeset_id, tags) VALUES (1003, ST_GeomFromText('MULTILINESTRING((333175.973956142 7395098.49130924,333188.494819187 7395102.10309665,333248.637266893 7395169.13708777))', 4326), 1003,
'{"name": "rua joao briccola", "start_date": "1930", "end_date": "1930"}');
INSERT INTO current_line (id, geom, fk_changeset_id, tags) VALUES (1004, ST_GeomFromText('MULTILINESTRING((333247.996555184 7395172.56160195,333255.762310051 7395178.46616912,333307.926051785 7395235.76603312,333354.472159794 7395273.32392717))', 4326), 1004,
'{"name": "ladeira porto geral", "start_date": "1930", "end_date": "1930"}');
INSERT INTO current_line (id, geom, fk_changeset_id, tags) VALUES (1005, ST_GeomFromText('MULTILINESTRING((333266.034554577 7395292.9053933,333308.06080675 7395235.87476644))', 4326), 1002,
'{"name": "travessa porto geral", "start_date": "1930", "end_date": "1930"}');
-- add way as GeoJSON
INSERT INTO current_line (id, geom, fk_changeset_id) 
VALUES (1006, 
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiLineString",
		    "coordinates":[[[-54, 33], [-32, 31], [-36, 89]]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	), 
	1002);
INSERT INTO current_line (id, geom, fk_changeset_id) 
VALUES (1007, 
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiLineString",
		    "coordinates":[[[-21, 56], [-32, 31], [-23, 74]]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	), 
	1003);



-- -----------------------------------------------------
-- Operations with current_way
-- -----------------------------------------------------

-- "remove" some lines
UPDATE current_line SET visible = FALSE WHERE id>=1003 AND id<=1007;



-- -----------------------------------------------------
-- Table current_polygon
-- -----------------------------------------------------
-- clean current_polygon table
DELETE FROM current_polygon;

-- add area
INSERT INTO current_polygon (id, geom, fk_changeset_id, tags) VALUES (1001, ST_GeomFromText('MULTIPOLYGON(((0 0, 1 1, 2 2, 3 3, 0 0)))', 4326), 1001,
'{"building": "hotel", "start_date": "1870", "end_date": "1900"}');
INSERT INTO current_polygon (id, geom, fk_changeset_id, tags) VALUES (1002, ST_GeomFromText('MULTIPOLYGON(((2 2, 3 3, 4 4, 5 5, 2 2)))', 4326), 1002,
'{"building": "theater", "start_date": "1920", "end_date": "1930"}');
-- add area as GeoJSON 
INSERT INTO current_polygon (id, geom, fk_changeset_id) 
VALUES (1006, 
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiPolygon",
		    "coordinates":[[[[-54, 33], [-32, 31], [-36, 89], [-54, 33]]]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	), 
	1003);
INSERT INTO current_polygon (id, geom, fk_changeset_id) 
VALUES (1007, 
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiPolygon",
		    "coordinates":[[[[-12, 32], [-21, 56], [-32, 31], [-23, 74], [-12, 32]]]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	), 
	1004);




-- -----------------------------------------------------
-- Operations with current_area
-- -----------------------------------------------------

-- "remove" some areas
UPDATE current_polygon SET visible = FALSE WHERE id>=1006 AND id<=1007;



-- -----------------------------------------------------
-- Final operations
-- -----------------------------------------------------
-- close the changesets
UPDATE changeset SET closed_at = '2017-12-01' WHERE id>=1001 AND id<=1004;

*/
