-- -----------------------------------------------------
-- Table user
-- -----------------------------------------------------
-- clean user table
DELETE FROM user_;

-- add users
INSERT INTO user_ (id, username, email, password, name) VALUES (1001, 'admin', 'admin@admin.com', 'admin', 'Administrator');
INSERT INTO user_ (id, username, email, password, name) VALUES (1002, 'rodrigo', 'rodrigo@admin.com', 'rodrigo', 'Rodrigo');

SELECT * FROM user_;
SELECT id, username, name FROM user_ WHERE email='admin@admin.com';

SELECT id, username, name FROM user_ WHERE email='admin@admin.c';


-- -----------------------------------------------------
-- Table project
-- -----------------------------------------------------
-- clean project table
DELETE FROM project;

-- add project
INSERT INTO project (id, name, description, fk_user_id_owner) VALUES (1001, 'default', 'default project', 1001);
INSERT INTO project (id, name, description, fk_user_id_owner) VALUES (1002, 'test_project', 'test_project', 1002);

-- SELECT * FROM project;


-- -----------------------------------------------------
-- Table changeset
-- -----------------------------------------------------
-- clean changeset table
DELETE FROM changeset;

-- add changeset with pre-id
INSERT INTO changeset (id, create_at, fk_project_id, fk_user_id_owner) VALUES (1001, '2017-10-20', 1001, 1001);
INSERT INTO changeset (id, create_at, fk_project_id, fk_user_id_owner) VALUES (1002, '2017-10-20', 1002, 1002) RETURNING id;

-- add changeset with SERIAL
-- INSERT INTO changeset (create_at, fk_project_id, fk_user_id_owner) VALUES ('2016-04-20', 1002, 1002) RETURNING id;

-- SELECTs
SELECT * FROM changeset;


-- -----------------------------------------------------
-- Table node
-- -----------------------------------------------------
-- clean node table
DELETE FROM node;

-- add node
INSERT INTO node (id, geom, version, fk_id_changeset) VALUES (1001, ST_GeomFromText('MULTIPOINT((-23.546421 -46.635722))', 4326), 1, 1001);
INSERT INTO node (id, geom, version, fk_id_changeset) VALUES (1002, ST_GeomFromText('MULTIPOINT((-23.55045 -46.634272))', 4326), 1, 1002);
INSERT INTO node (id, geom, version, visible, fk_id_changeset) VALUES (1003, ST_GeomFromText('MULTIPOINT((-23.542626 -46.638684))', 4326), 1, FALSE, 1001);
INSERT INTO node (id, geom, version, visible, fk_id_changeset) VALUES (1004, ST_GeomFromText('MULTIPOINT((-23.547951 -46.634215))', 4326), 1, FALSE, 1002);
INSERT INTO node (id, geom, version, visible, fk_id_changeset) VALUES (1005, ST_GeomFromText('MULTIPOINT((-23.530159 -46.654885))', 4326), 1, FALSE, 1002);

-- SELECTs
-- SELECT * FROM node;
-- SELECT id, geom, visible, version, fk_id_changeset FROM node;

-- -----------------------------------------------------
-- Table node_tag
-- -----------------------------------------------------
-- clean node_tag table
DELETE FROM node_tag;

-- insert values in table node_tag
-- SOURCE: AialaLevy_theaters20170710.xlsx
-- node 1
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1001, 'address', 'R. São José', 1001, 1);
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1002, 'start_date', '1869', 1001, 1);
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1003, 'end_date', '1869', 1001, 1);
-- node 2
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1004, 'address', 'R. Marechal Deodoro', 1002, 1);
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1005, 'start_date', '1878', 1002, 1);
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1006, 'end_date', '1910', 1002, 1);
-- node 3
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1007, 'address', 'R. 11 de Junho, 9 = D. José de Barros', 1003, 1);
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1008, 'start_date', '1886', 1003, 1);
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1009, 'end_date', '1916', 1003, 1);
-- node 4
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1010, 'address', 'R. 15 de Novembro, 17A', 1004, 1);
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1011, 'start_date', '1890', 1004, 1);
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1012, 'end_date', '1911', 1004, 1);
-- node 5
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1013, 'address', 'R. Barra Funda, 74', 1005, 1);
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1014, 'start_date', '1897', 1005, 1);
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1015, 'end_date', '1897', 1005, 1);

--SELECT * FROM node_tag;


-- -----------------------------------------------------
-- Table way
-- -----------------------------------------------------
-- clean way table
DELETE FROM way;

-- add node
INSERT INTO way (id, geom, version, fk_id_changeset) VALUES (1001, ST_GeomFromText('MULTILINESTRING((333188.261004703 7395284.32488995,333205.817689791 7395247.71277836,333247.996555184 7395172.56160195,333261.133400433 7395102.3470075,333270.981533908 7395034.48052247,333277.885095545 7394986.25678192))', 4326), 1, 1001);
INSERT INTO way (id, geom, version, fk_id_changeset) VALUES (1002, ST_GeomFromText('MULTILINESTRING((333270.653184563 7395036.74327773,333244.47769325 7395033.35326418,333204.141105934 7395028.41654752,333182.467715735 7395026.2492085))', 4326), 1, 1002);
INSERT INTO way (id, geom, version, visible, fk_id_changeset) VALUES (1003, ST_GeomFromText('MULTILINESTRING((333175.973956142 7395098.49130924,333188.494819187 7395102.10309665,333248.637266893 7395169.13708777))', 4326), 1, FALSE, 1001);
INSERT INTO way (id, geom, version, visible, fk_id_changeset) VALUES (1004, ST_GeomFromText('MULTILINESTRING((333247.996555184 7395172.56160195,333255.762310051 7395178.46616912,333307.926051785 7395235.76603312,333354.472159794 7395273.32392717))', 4326), 1, FALSE, 1002);
INSERT INTO way (id, geom, version, visible, fk_id_changeset) VALUES (1005, ST_GeomFromText('MULTILINESTRING((333266.034554577 7395292.9053933,333308.06080675 7395235.87476644))', 4326), 1, FALSE, 1002);

-- SELECTs
-- SELECT * FROM way;
-- SELECT id, geom, visible, version, fk_id_changeset FROM way;

-- -----------------------------------------------------
-- Table way_tag
-- -----------------------------------------------------
-- clean way_tag table
DELETE FROM way_tag;

-- insert values in table way_tag
-- SOURCE: db_pauliceia
-- way 1
INSERT INTO way_tag (id, k, v, fk_way_id, fk_way_version) VALUES (1001, 'name', 'rua boa vista', 1001, 1);
INSERT INTO way_tag (id, k, v, fk_way_id, fk_way_version) VALUES (1002, 'start_date', '1930', 1001, 1);
INSERT INTO way_tag (id, k, v, fk_way_id, fk_way_version) VALUES (1003, 'end_date', '1930', 1001, 1);
-- way 2
INSERT INTO way_tag (id, k, v, fk_way_id, fk_way_version) VALUES (1004, 'address', 'rua tres de dezembro', 1002, 1);
INSERT INTO way_tag (id, k, v, fk_way_id, fk_way_version) VALUES (1005, 'start_date', '1930', 1002, 1);
INSERT INTO way_tag (id, k, v, fk_way_id, fk_way_version) VALUES (1006, 'end_date', '1930', 1002, 1);
-- way 3
INSERT INTO way_tag (id, k, v, fk_way_id, fk_way_version) VALUES (1007, 'address', 'rua joao briccola', 1003, 1);
INSERT INTO way_tag (id, k, v, fk_way_id, fk_way_version) VALUES (1008, 'start_date', '1930', 1003, 1);
INSERT INTO way_tag (id, k, v, fk_way_id, fk_way_version) VALUES (1009, 'end_date', '1930', 1003, 1);
-- way 4
INSERT INTO way_tag (id, k, v, fk_way_id, fk_way_version) VALUES (1010, 'address', 'ladeira porto geral', 1004, 1);
INSERT INTO way_tag (id, k, v, fk_way_id, fk_way_version) VALUES (1011, 'start_date', '1930', 1004, 1);
INSERT INTO way_tag (id, k, v, fk_way_id, fk_way_version) VALUES (1012, 'end_date', '1930', 1004, 1);
-- way 5
INSERT INTO way_tag (id, k, v, fk_way_id, fk_way_version) VALUES (1013, 'address', 'travessa porto geral', 1005, 1);
INSERT INTO way_tag (id, k, v, fk_way_id, fk_way_version) VALUES (1014, 'start_date', '1930', 1005, 1);
INSERT INTO way_tag (id, k, v, fk_way_id, fk_way_version) VALUES (1015, 'end_date', '1930', 1005, 1);

--SELECT * FROM way_tag;










-- -----------------------------------------------------
-- Table area
-- -----------------------------------------------------
-- clean area table
DELETE FROM area;

-- add node
INSERT INTO area (id, geom, version, fk_id_changeset) VALUES (1001, ST_GeomFromText('MULTIPOLYGON(((0 0, 1 1, 2 2, 3 3, 0 0)))', 4326), 1, 1001);
INSERT INTO area (id, geom, version, fk_id_changeset) VALUES (1002, ST_GeomFromText('MULTIPOLYGON(((2 2, 3 3, 4 4, 5 5, 2 2)))', 4326), 1, 1002);

-- SELECTs
-- SELECT * FROM area;
-- SELECT id, geom, visible, version, fk_id_changeset FROM area;

-- -----------------------------------------------------
-- Table area_tag
-- -----------------------------------------------------
-- clean area_tag table
DELETE FROM area_tag;

-- insert values in table area_tag
-- SOURCE: -
-- node 1
INSERT INTO area_tag (id, k, v, fk_area_id, fk_area_version) VALUES (1001, 'building', 'hotel', 1001, 1);
INSERT INTO area_tag (id, k, v, fk_area_id, fk_area_version) VALUES (1002, 'start_date', '1870', 1001, 1);
INSERT INTO area_tag (id, k, v, fk_area_id, fk_area_version) VALUES (1003, 'end_date', '1900', 1001, 1);
-- node 2
INSERT INTO area_tag (id, k, v, fk_area_id, fk_area_version) VALUES (1004, 'building', 'theater', 1002, 1);
INSERT INTO area_tag (id, k, v, fk_area_id, fk_area_version) VALUES (1005, 'start_date', '1920', 1002, 1);
INSERT INTO area_tag (id, k, v, fk_area_id, fk_area_version) VALUES (1006, 'end_date', '1930', 1002, 1);

--SELECT * FROM area_tag;




-- -----------------------------------------------------
-- Queries about table {node,way,area}
-- -----------------------------------------------------
/*
-- get result in WKT
-- 'p' means 'properties'
SELECT p.id, ST_AsText(p.geom) as geom, p.visible, 
p.version, p.fk_id_changeset 
FROM node As p WHERE p.id = 1;

-- get list of GEOJSON
-- 'p' means 'properties'
SELECT row_to_json(fc)
FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features
	FROM (
		SELECT 'Feature' As type,  -- type field
		ST_AsGeoJSON(geom)::json As geometry,  -- geometry field
		row_to_json(
			(SELECT p FROM (SELECT p.id, p.visible, p.version, p.fk_id_changeset) As p)
			) As properties  -- properties field
		FROM node As p WHERE p.id = 1
	) As f 
) As fc;

-- get list of GEOJSON with tags
SELECT jsonb_build_object(
    'type',       'FeatureCollection',
    'features',   jsonb_agg(jsonb_build_object(
        'type',       'Feature',
        'geometry',   ST_AsGeoJSON(node.geom)::jsonb,
        'properties', to_jsonb(node) - 'geom' - 'visible' - 'version',
        'tags',       tags.jsontags
    ))
) AS row_to_json
FROM node
CROSS JOIN LATERAL (
	SELECT json_agg(json_build_object('id', id, 'k', k, 'v', v)) AS jsontags 
	FROM node_tag 
	WHERE fk_node_id = node.id    
) AS tags
WHERE id=1;
*/




