
-- -----------------------------------------------------
-- Table user
-- -----------------------------------------------------
-- clean user table
DELETE FROM user_;

-- add users
INSERT INTO user_ (id, username, email, password, name) VALUES (1001, 'admin', 'admin@admin.com', 'admin', 'Administrator');
INSERT INTO user_ (id, username, email, password, name) VALUES (1002, 'rodrigo', 'rodrigo@admin.com', 'rodrigo', 'Rodrigo');
INSERT INTO user_ (id, username, email, password, name) VALUES (1003, 'miguel', 'miguel@admin.com', 'miguel', 'Miguel');
INSERT INTO user_ (id, username, email, password, name) VALUES (1004, 'rafael', 'rafael@admin.com', 'rafael', 'Rafael');
INSERT INTO user_ (id, username, email, password, name) VALUES (1005, 'gabriel', 'gabriel@admin.com', 'gabriel', 'Gabriel');

-- SELECT * FROM user_;
-- SELECT id, username, name FROM user_ WHERE email='admin@admin.com';
-- SELECT id, username, name FROM user_ WHERE email='admin@admin.c';


-- -----------------------------------------------------
-- Table project
-- -----------------------------------------------------
-- clean project table
DELETE FROM project;

-- add project
INSERT INTO project (id, create_at, fk_user_id_owner) VALUES (1001, '2017-11-20', 1001);
INSERT INTO project (id, create_at, fk_user_id_owner) VALUES (1002, '2017-10-12', 1002);
INSERT INTO project (id, create_at, fk_user_id_owner) VALUES (1003, '2017-12-23', 1002);
INSERT INTO project (id, create_at, fk_user_id_owner) VALUES (1004, '2017-09-11', 1003);
INSERT INTO project (id, create_at, fk_user_id_owner) VALUES (1005, '2017-06-04', 1003);

-- SELECT * FROM project;
-- SELECT * FROM project p WHERE p.id = 1001;


-- -----------------------------------------------------
-- Table project_tag
-- -----------------------------------------------------
-- clean project_tag table
DELETE FROM project_tag;

-- insert values in table project_tag
-- SOURCE: -
-- project 1001
INSERT INTO project_tag (id, k, v, fk_project_id) VALUES (1001, 'name', 'default', 1001);
INSERT INTO project_tag (id, k, v, fk_project_id) VALUES (1002, 'description', 'default project', 1001);
-- project 1002
INSERT INTO project_tag (id, k, v, fk_project_id) VALUES (1003, 'name', 'test_project', 1002);
INSERT INTO project_tag (id, k, v, fk_project_id) VALUES (1004, 'description', 'test_project', 1002);
-- project 1003
INSERT INTO project_tag (id, k, v, fk_project_id) VALUES (1005, 'name', 'project 3', 1003);
INSERT INTO project_tag (id, k, v, fk_project_id) VALUES (1006, 'description', 'test_project', 1003);
-- project 1004
INSERT INTO project_tag (id, k, v, fk_project_id) VALUES (1007, 'name', 'project 4', 1004);
INSERT INTO project_tag (id, k, v, fk_project_id) VALUES (1008, 'description', 'test_project', 1004);
-- project 1005
INSERT INTO project_tag (id, k, v, fk_project_id) VALUES (1009, 'name', 'project 5', 1005);
INSERT INTO project_tag (id, k, v, fk_project_id) VALUES (1010, 'description', 'test_project', 1005);


-- SELECT * FROM project_tag;

/*
SELECT p.id, p.create_at, p.removed_at FROM project p WHERE p.id = 1003;
SELECT p.id, date(create_at) AS myTime, p.removed_at FROM project p WHERE p.id = 1003;
SELECT p.id, to_char(create_at, 'YYYY-MM-DD HH24:MI:SS') as create_at, to_char(removed_at, 'YYYY-MM-DD HH24:MI:SS') as removed_at FROM project p WHERE p.id = 1003;
*/

-- UPDATE project SET visible = FALSE, removed_at=LOCALTIMESTAMP WHERE id=1001;


-- SELECT p.id, p.create_at, p.closed_at, ṕt.id, pt.k, pt.v FROM project p, project_tag pt WHERE p.id = pt.fk_project_id;


/*
SELECT jsonb_build_object(
    'type', 'FeatureCollection',
    'features',   jsonb_agg(jsonb_build_object(
        'type',       'Project',
        'properties', json_build_object(
            'id', id,
            'create_at',  to_char(create_at, 'YYYY-MM-DD HH24:MI:SS'),
            'removed_at', to_char(removed_at, 'YYYY-MM-DD HH24:MI:SS'),
            'fk_user_id_owner', fk_user_id_owner
        ),
        'tags',       tags.jsontags
    ))
) AS row_to_json
FROM project
CROSS JOIN LATERAL (
	SELECT json_agg(json_build_object('k', k, 'v', v)) AS jsontags 
	FROM project_tag 
	WHERE fk_project_id = project.id    
) AS tags
WHERE id=1001;
*/


-- -----------------------------------------------------
-- Table changeset
-- -----------------------------------------------------
-- clean changeset table
DELETE FROM changeset;

-- add changeset open
INSERT INTO changeset (id, create_at, fk_project_id, fk_user_id_owner) VALUES (1001, '2017-10-20', 1001, 1001);
INSERT INTO changeset (id, create_at, fk_project_id, fk_user_id_owner) VALUES (1002, '2017-10-20', 1002, 1002);
INSERT INTO changeset (id, create_at, fk_project_id, fk_user_id_owner) VALUES (1003, LOCALTIMESTAMP, 1001, 1001);
INSERT INTO changeset (id, create_at, fk_project_id, fk_user_id_owner) VALUES (1004, LOCALTIMESTAMP, 1002, 1002);

-- SELECT * FROM changeset;


-- -----------------------------------------------------
-- Table changeset_tag
-- -----------------------------------------------------
-- clean changeset_tag table
DELETE FROM changeset_tag;

-- insert values in table changeset_tag
-- SOURCE: -
-- changeset 1001
INSERT INTO changeset_tag (id, k, v, fk_changeset_id) VALUES (1001, 'created_by', 'pauliceia_portal', 1001);
INSERT INTO changeset_tag (id, k, v, fk_changeset_id) VALUES (1002, 'comment', 'a changeset created', 1001);
-- changeset 1002
INSERT INTO changeset_tag (id, k, v, fk_changeset_id) VALUES (1003, 'created_by', 'test_postgresql', 1002);
INSERT INTO changeset_tag (id, k, v, fk_changeset_id) VALUES (1004, 'comment', 'changeset test', 1002);
-- changeset 1003
INSERT INTO changeset_tag (id, k, v, fk_changeset_id) VALUES (1005, 'created_by', 'pauliceia_portal', 1003);
INSERT INTO changeset_tag (id, k, v, fk_changeset_id) VALUES (1006, 'comment', 'a changeset created', 1003);
-- changeset 1004
INSERT INTO changeset_tag (id, k, v, fk_changeset_id) VALUES (1007, 'created_by', 'test_postgresql', 1004);
INSERT INTO changeset_tag (id, k, v, fk_changeset_id) VALUES (1008, 'comment', 'changeset test', 1004);

-- SELECT * FROM changeset_tag;

--SELECT c.id, c.create_at, c.closed_at, ct.id, ct.k, ct.v;
--FROM changeset c, changeset_tag ct WHERE c.id = ct.fk_changeset_id;



-- -----------------------------------------------------
-- Table current_node
-- -----------------------------------------------------
-- clean current_node table
DELETE FROM current_node;

-- add node
INSERT INTO current_node (id, geom, fk_changeset_id) VALUES (1001, ST_GeomFromText('MULTIPOINT((-23.546421 -46.635722))', 4326), 1001);
INSERT INTO current_node (id, geom, fk_changeset_id) VALUES (1002, ST_GeomFromText('MULTIPOINT((-23.55045 -46.634272))', 4326), 1002);
INSERT INTO current_node (id, geom, fk_changeset_id) VALUES (1003, ST_GeomFromText('MULTIPOINT((-23.542626 -46.638684))', 4326), 1003);
INSERT INTO current_node (id, geom, fk_changeset_id) VALUES (1004, ST_GeomFromText('MULTIPOINT((-23.547951 -46.634215))', 4326), 1004);
INSERT INTO current_node (id, geom, fk_changeset_id) VALUES (1005, ST_GeomFromText('MULTIPOINT((-23.530159 -46.654885))', 4326), 1001);
-- add node as GeoJSON
INSERT INTO current_node (id, geom, fk_changeset_id) 
VALUES (1006, 
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiPoint",
		    "coordinates":[[-54, 33]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	), 
	1003);
INSERT INTO current_node (id, geom, fk_changeset_id) 
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
-- Table current_node_tag
-- -----------------------------------------------------
-- clean current_node_tag table
DELETE FROM current_node_tag;

-- insert values in table node_tag
-- SOURCE: AialaLevy_theaters20170710.xlsx
-- node 1001
INSERT INTO current_node_tag (id, k, v, fk_current_node_id) VALUES (1001, 'address', 'R. São José', 1001);
INSERT INTO current_node_tag (id, k, v, fk_current_node_id) VALUES (1002, 'start_date', '1869', 1001);
INSERT INTO current_node_tag (id, k, v, fk_current_node_id) VALUES (1003, 'end_date', '1869', 1001);
-- node 1002
INSERT INTO current_node_tag (id, k, v, fk_current_node_id) VALUES (1004, 'address', 'R. Marechal Deodoro', 1002);
INSERT INTO current_node_tag (id, k, v, fk_current_node_id) VALUES (1005, 'start_date', '1878', 1002);
INSERT INTO current_node_tag (id, k, v, fk_current_node_id) VALUES (1006, 'end_date', '1910', 1002);
-- node 1003
INSERT INTO current_node_tag (id, k, v, fk_current_node_id) VALUES (1007, 'address', 'R. 11 de Junho, 9 = D. José de Barros', 1003);
INSERT INTO current_node_tag (id, k, v, fk_current_node_id) VALUES (1008, 'start_date', '1886', 1003);
INSERT INTO current_node_tag (id, k, v, fk_current_node_id) VALUES (1009, 'end_date', '1916', 1003);
-- node 1004
INSERT INTO current_node_tag (id, k, v, fk_current_node_id) VALUES (1010, 'address', 'R. 15 de Novembro, 17A', 1004);
INSERT INTO current_node_tag (id, k, v, fk_current_node_id) VALUES (1011, 'start_date', '1890', 1004);
INSERT INTO current_node_tag (id, k, v, fk_current_node_id) VALUES (1012, 'end_date', '1911', 1004);
-- node 1005
INSERT INTO current_node_tag (id, k, v, fk_current_node_id) VALUES (1013, 'address', 'R. Barra Funda, 74', 1005);
INSERT INTO current_node_tag (id, k, v, fk_current_node_id) VALUES (1014, 'start_date', '1897', 1005);
INSERT INTO current_node_tag (id, k, v, fk_current_node_id) VALUES (1015, 'end_date', '1897', 1005);


-- -----------------------------------------------------
-- Operations with current_node
-- -----------------------------------------------------

-- SELECT * FROM current_node n WHERE visible=TRUE;

-- get just the valid nodes
-- SELECT n.id, ST_AsText(n.geom) as geom, n.version, n.fk_changeset_id, n.visible FROM current_node n WHERE visible=TRUE;

-- SELECT n.id, ST_AsText(n.geom) as geom, n.version, n.fk_changeset_id, nt.id, nt.k, nt.v FROM current_node n, node_tag nt WHERE n.id = nt.fk_node_id;

--SELECT * FROM current_node_tag;

-- "remove" some nodes
UPDATE current_node SET visible = FALSE WHERE id>=1003 AND id<=1005;






/*
-- -----------------------------------------------------
-- Table node
-- -----------------------------------------------------
-- clean node table
DELETE FROM node;

-- add node
INSERT INTO node (id, geom, fk_changeset_id) VALUES (1001, ST_GeomFromText('MULTIPOINT((-23.546421 -46.635722))', 4326), 1001);
INSERT INTO node (id, geom, fk_changeset_id) VALUES (1002, ST_GeomFromText('MULTIPOINT((-23.55045 -46.634272))', 4326), 1002);
INSERT INTO node (id, geom, visible, fk_changeset_id) VALUES (1003, ST_GeomFromText('MULTIPOINT((-23.542626 -46.638684))', 4326), FALSE, 1001);
INSERT INTO node (id, geom, visible, fk_changeset_id) VALUES (1004, ST_GeomFromText('MULTIPOINT((-23.547951 -46.634215))', 4326), FALSE, 1002);
INSERT INTO node (id, geom, visible, fk_changeset_id) VALUES (1005, ST_GeomFromText('MULTIPOINT((-23.530159 -46.654885))', 4326), FALSE, 1002);
-- add node as GeoJSON
INSERT INTO node (id, geom, visible, fk_changeset_id) 
VALUES (1006, 
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiPoint",
		    "coordinates":[[-54, 33]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	), 
	FALSE, 1002);

INSERT INTO node (id, geom, visible, fk_changeset_id) 
VALUES (1007, 
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiPoint",
		    "coordinates":[[-54, 33]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	), 
	FALSE, 1002);

-- SELECT
SELECT n.id, ST_AsText(n.geom) as geom, n.version, n.fk_changeset_id, n.visible FROM node n;
-- SELECT n.id, ST_AsText(n.geom) as geom, n.version, n.fk_changeset_id, nt.id, nt.k, nt.v FROM node n, node_tag nt WHERE n.id = nt.fk_node_id;

-- DELETE
-- UPDATE node SET visible = FALSE WHERE id=7;



-- -----------------------------------------------------
-- Table node_tag
-- -----------------------------------------------------
-- clean node_tag table
DELETE FROM node_tag;

-- insert values in table node_tag
-- SOURCE: AialaLevy_theaters20170710.xlsx
-- node 1001
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1001, 'address', 'R. São José', 1001, 1);
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1002, 'start_date', '1869', 1001, 1);
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1003, 'end_date', '1869', 1001, 1);
-- node 1002
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1004, 'address', 'R. Marechal Deodoro', 1002, 1);
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1005, 'start_date', '1878', 1002, 1);
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1006, 'end_date', '1910', 1002, 1);
-- node 1003
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1007, 'address', 'R. 11 de Junho, 9 = D. José de Barros', 1003, 1);
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1008, 'start_date', '1886', 1003, 1);
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1009, 'end_date', '1916', 1003, 1);
-- node 1004
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1010, 'address', 'R. 15 de Novembro, 17A', 1004, 1);
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1011, 'start_date', '1890', 1004, 1);
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1012, 'end_date', '1911', 1004, 1);
-- node 1005
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1013, 'address', 'R. Barra Funda, 74', 1005, 1);
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1014, 'start_date', '1897', 1005, 1);
INSERT INTO node_tag (id, k, v, fk_node_id, fk_node_version) VALUES (1015, 'end_date', '1897', 1005, 1);

--SELECT * FROM node_tag;

*/







-- -----------------------------------------------------
-- Table current_way
-- -----------------------------------------------------
-- clean current_way table
DELETE FROM current_way;

-- add way
INSERT INTO current_way (id, geom, fk_changeset_id) VALUES (1001, ST_GeomFromText('MULTILINESTRING((333188.261004703 7395284.32488995,333205.817689791 7395247.71277836,333247.996555184 7395172.56160195,333261.133400433 7395102.3470075,333270.981533908 7395034.48052247,333277.885095545 7394986.25678192))', 4326), 1001);
INSERT INTO current_way (id, geom, fk_changeset_id) VALUES (1002, ST_GeomFromText('MULTILINESTRING((333270.653184563 7395036.74327773,333244.47769325 7395033.35326418,333204.141105934 7395028.41654752,333182.467715735 7395026.2492085))', 4326), 1002);
INSERT INTO current_way (id, geom, fk_changeset_id) VALUES (1003, ST_GeomFromText('MULTILINESTRING((333175.973956142 7395098.49130924,333188.494819187 7395102.10309665,333248.637266893 7395169.13708777))', 4326), 1003);
INSERT INTO current_way (id, geom, fk_changeset_id) VALUES (1004, ST_GeomFromText('MULTILINESTRING((333247.996555184 7395172.56160195,333255.762310051 7395178.46616912,333307.926051785 7395235.76603312,333354.472159794 7395273.32392717))', 4326), 1004);
INSERT INTO current_way (id, geom, fk_changeset_id) VALUES (1005, ST_GeomFromText('MULTILINESTRING((333266.034554577 7395292.9053933,333308.06080675 7395235.87476644))', 4326), 1002);
-- add way as GeoJSON
INSERT INTO current_way (id, geom, fk_changeset_id) 
VALUES (1006, 
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiLineString",
		    "coordinates":[[[-54, 33], [-32, 31], [-36, 89]]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	), 
	1002);
INSERT INTO current_way (id, geom, fk_changeset_id) 
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
-- Table current_way_tag
-- -----------------------------------------------------
-- clean current_way_tag table
DELETE FROM current_way_tag;

-- insert values in table way_tag
-- SOURCE: db_pauliceia
-- way 1
INSERT INTO current_way_tag (id, k, v, fk_current_way_id) VALUES (1001, 'name', 'rua boa vista', 1001);
INSERT INTO current_way_tag (id, k, v, fk_current_way_id) VALUES (1002, 'start_date', '1930', 1001);
INSERT INTO current_way_tag (id, k, v, fk_current_way_id) VALUES (1003, 'end_date', '1930', 1001);
-- way 2
INSERT INTO current_way_tag (id, k, v, fk_current_way_id) VALUES (1004, 'address', 'rua tres de dezembro', 1002);
INSERT INTO current_way_tag (id, k, v, fk_current_way_id) VALUES (1005, 'start_date', '1930', 1002);
INSERT INTO current_way_tag (id, k, v, fk_current_way_id) VALUES (1006, 'end_date', '1930', 1002);
-- way 3
INSERT INTO current_way_tag (id, k, v, fk_current_way_id) VALUES (1007, 'address', 'rua joao briccola', 1003);
INSERT INTO current_way_tag (id, k, v, fk_current_way_id) VALUES (1008, 'start_date', '1930', 1003);
INSERT INTO current_way_tag (id, k, v, fk_current_way_id) VALUES (1009, 'end_date', '1930', 1003);
-- way 4
INSERT INTO current_way_tag (id, k, v, fk_current_way_id) VALUES (1010, 'address', 'ladeira porto geral', 1004);
INSERT INTO current_way_tag (id, k, v, fk_current_way_id) VALUES (1011, 'start_date', '1930', 1004);
INSERT INTO current_way_tag (id, k, v, fk_current_way_id) VALUES (1012, 'end_date', '1930', 1004);
-- way 5
INSERT INTO current_way_tag (id, k, v, fk_current_way_id) VALUES (1013, 'address', 'travessa porto geral', 1005);
INSERT INTO current_way_tag (id, k, v, fk_current_way_id) VALUES (1014, 'start_date', '1930', 1005);
INSERT INTO current_way_tag (id, k, v, fk_current_way_id) VALUES (1015, 'end_date', '1930', 1005);


-- -----------------------------------------------------
-- Operations with current_way
-- -----------------------------------------------------

-- get just the valid nodes
-- SELECT id, geom, visible, version, fk_changeset_id FROM current_way WHERE visible=TRUE;

-- SELECT id, ST_AsText(geom) as geom, version, fk_changeset_id FROM way;
-- SELECT w.id, ST_AsText(w.geom) as geom, w.version, w.fk_changeset_id, wt.id, wt.k, wt.v FROM way w, way_tag wt WHERE w.id = wt.fk_way_id;

-- "remove" some ways
UPDATE current_way SET visible = FALSE WHERE id>=1003 AND id<=1007;

--SELECT * FROM way_tag;



/*
-- -----------------------------------------------------
-- Table way
-- -----------------------------------------------------
-- clean way table
DELETE FROM way;

-- add way
INSERT INTO way (id, geom, fk_changeset_id) VALUES (1001, ST_GeomFromText('MULTILINESTRING((333188.261004703 7395284.32488995,333205.817689791 7395247.71277836,333247.996555184 7395172.56160195,333261.133400433 7395102.3470075,333270.981533908 7395034.48052247,333277.885095545 7394986.25678192))', 4326), 1001);
INSERT INTO way (id, geom, fk_changeset_id) VALUES (1002, ST_GeomFromText('MULTILINESTRING((333270.653184563 7395036.74327773,333244.47769325 7395033.35326418,333204.141105934 7395028.41654752,333182.467715735 7395026.2492085))', 4326), 1002);
INSERT INTO way (id, geom, visible, fk_changeset_id) VALUES (1003, ST_GeomFromText('MULTILINESTRING((333175.973956142 7395098.49130924,333188.494819187 7395102.10309665,333248.637266893 7395169.13708777))', 4326), FALSE, 1001);
INSERT INTO way (id, geom, visible, fk_changeset_id) VALUES (1004, ST_GeomFromText('MULTILINESTRING((333247.996555184 7395172.56160195,333255.762310051 7395178.46616912,333307.926051785 7395235.76603312,333354.472159794 7395273.32392717))', 4326), FALSE, 1002);
INSERT INTO way (id, geom, visible, fk_changeset_id) VALUES (1005, ST_GeomFromText('MULTILINESTRING((333266.034554577 7395292.9053933,333308.06080675 7395235.87476644))', 4326), FALSE, 1002);
-- add way as GeoJSON
INSERT INTO way (id, geom, visible, fk_changeset_id) 
VALUES (1006, 
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiLineString",
		    "coordinates":[[[-54, 33], [-32, 31], [-36, 89]]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	), 
	FALSE, 1002);
INSERT INTO way (id, geom, visible, fk_changeset_id) 
VALUES (1007, 
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiLineString",
		    "coordinates":[[[-21, 56], [-32, 31], [-23, 74]]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	), 
	FALSE, 1002);

-- SELECTs
-- SELECT * FROM way;
-- SELECT id, geom, visible, version, fk_changeset_id FROM way;
-- SELECT id, ST_AsText(geom) as geom, version, fk_changeset_id FROM way;
-- SELECT w.id, ST_AsText(w.geom) as geom, w.version, w.fk_changeset_id, wt.id, wt.k, wt.v FROM way w, way_tag wt WHERE w.id = wt.fk_way_id;


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
*/





-- -----------------------------------------------------
-- Table current_area
-- -----------------------------------------------------
-- clean current_area table
DELETE FROM current_area;

-- add area
INSERT INTO current_area (id, geom, fk_changeset_id) VALUES (1001, ST_GeomFromText('MULTIPOLYGON(((0 0, 1 1, 2 2, 3 3, 0 0)))', 4326), 1001);
INSERT INTO current_area (id, geom, fk_changeset_id) VALUES (1002, ST_GeomFromText('MULTIPOLYGON(((2 2, 3 3, 4 4, 5 5, 2 2)))', 4326), 1002);
-- add area as GeoJSON 
INSERT INTO current_area (id, geom, fk_changeset_id) 
VALUES (1006, 
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiPolygon",
		    "coordinates":[[[[-54, 33], [-32, 31], [-36, 89], [-54, 33]]]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	), 
	1003);
INSERT INTO current_area (id, geom, fk_changeset_id) 
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
-- Table current_area_tag
-- -----------------------------------------------------
-- clean current_area_tag table
DELETE FROM current_area_tag;

-- insert values in table area_tag
-- SOURCE: -
-- area 1
INSERT INTO current_area_tag (id, k, v, fk_current_area_id) VALUES (1001, 'building', 'hotel', 1001);
INSERT INTO current_area_tag (id, k, v, fk_current_area_id) VALUES (1002, 'start_date', '1870', 1001);
INSERT INTO current_area_tag (id, k, v, fk_current_area_id) VALUES (1003, 'end_date', '1900', 1001);
-- area 2
INSERT INTO current_area_tag (id, k, v, fk_current_area_id) VALUES (1004, 'building', 'theater', 1002);
INSERT INTO current_area_tag (id, k, v, fk_current_area_id) VALUES (1005, 'start_date', '1920', 1002);
INSERT INTO current_area_tag (id, k, v, fk_current_area_id) VALUES (1006, 'end_date', '1930', 1002);


-- -----------------------------------------------------
-- Operations with current_area
-- -----------------------------------------------------

-- get just the valid nodes
-- SELECT id, geom, visible, version, fk_changeset_id FROM current_area WHERE visible=TRUE;

-- SELECT id, ST_AsText(geom) as geom, version, fk_changeset_id FROM area;
-- SELECT a.id, ST_AsText(a.geom) as geom, a.version, a.fk_changeset_id, at.id, at.k, at.v FROM area a, area_tag at WHERE a.id = at.fk_area_id;

-- "remove" some areas
UPDATE current_area SET visible = FALSE WHERE id>=1006 AND id<=1007;





/*
-- -----------------------------------------------------
-- Table area
-- -----------------------------------------------------
-- clean area table
DELETE FROM area;

-- add area
INSERT INTO area (id, geom, fk_changeset_id) VALUES (1001, ST_GeomFromText('MULTIPOLYGON(((0 0, 1 1, 2 2, 3 3, 0 0)))', 4326), 1001);
INSERT INTO area (id, geom, fk_changeset_id) VALUES (1002, ST_GeomFromText('MULTIPOLYGON(((2 2, 3 3, 4 4, 5 5, 2 2)))', 4326), 1002);
-- add area as GeoJSON 
INSERT INTO area (id, geom, visible, fk_changeset_id) 
VALUES (1006, 
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiPolygon",
		    "coordinates":[[[[-54, 33], [-32, 31], [-36, 89], [-54, 33]]]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	), 
	FALSE, 1002);
INSERT INTO area (id, geom, visible, fk_changeset_id) 
VALUES (1007, 
	ST_GeomFromGeoJSON(
		'{
		    "type":"MultiPolygon",
		    "coordinates":[[[[-12, 32], [-21, 56], [-32, 31], [-23, 74], [-12, 32]]]],
		    "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
		}'
	), 
	FALSE, 1002);

-- SELECTs
-- SELECT * FROM area;
-- SELECT id, geom, visible, version, fk_changeset_id FROM area;
-- SELECT id, ST_AsText(geom) as geom, version, fk_changeset_id FROM area;
-- SELECT a.id, ST_AsText(a.geom) as geom, a.version, a.fk_changeset_id, at.id, at.k, at.v FROM area a, area_tag at WHERE a.id = at.fk_area_id;


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
*/




-- -----------------------------------------------------
-- Final operations
-- -----------------------------------------------------
-- close the changesets
UPDATE changeset SET closed_at = LOCALTIMESTAMP WHERE id>=1001 AND id<=1004;




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
WHERE id=1001;

SELECT jsonb_build_object(
    'type', 'FeatureCollection',
    'crs',  json_build_object(
        'type',      'name', 
        'properties', json_build_object(
            'name', 'EPSG:4326'
        )
    ),
    'features',   jsonb_agg(jsonb_build_object(
        'type',       'Feature',
        'geometry',   ST_AsGeoJSON(geom)::jsonb,
        'properties', json_build_object(
            'id', id,
            'fk_changeset_id', fk_changeset_id
        ),
        'tags',       tags.jsontags
    ))
) AS row_to_json
FROM current_node
CROSS JOIN LATERAL (
	SELECT json_agg(json_build_object('k', k, 'v', v)) AS jsontags 
	FROM current_node_tag 
	WHERE fk_current_node_id = current_node.id    
) AS tags
WHERE current_node.id=1001;
*/


/*
SELECT jsonb_build_object(
    'type', 'FeatureCollection',
    'crs',  json_build_object(
        'type',      'name', 
        'properties', json_build_object(
            'name', 'EPSG:4326'
        )
    ),
    'features',   jsonb_agg(jsonb_build_object(
        'type',       'Feature',
        'geometry',   ST_AsGeoJSON(geom)::jsonb,
        'properties', json_build_object(
            'id', id,
            'fk_changeset_id', fk_changeset_id
        ),
        'tags',       tags.jsontags
    ))
) AS row_to_json
FROM (
    -- (1) get all elements with its changeset information
    SELECT c.id, c.geom, c.fk_changeset_id
    FROM current_node c LEFT JOIN changeset cs ON c.fk_changeset_id = cs.id
    WHERE c.visible=TRUE AND c.id=1001
) AS element
CROSS JOIN LATERAL (
    -- (2) get the tags of some element
	SELECT json_agg(json_build_object('k', k, 'v', v)) AS jsontags 
	FROM current_node_tag 
	WHERE fk_current_node_id = element.id    
) AS tags;
*/

-- all changeset
-- SELECT * FROM changeset;
-- just changeset open
-- SELECT * FROM changeset WHERE closed_at is NULL;
-- just changeset close
-- SELECT * FROM changeset WHERE closed_at is not NULL;


-- get all nodes with its changeset information
/*
SELECT cn.id, cn.visible, cn.fk_changeset_id, 
        cs. id, cs.create_at, cs.closed_at, cs.fk_user_id_owner
FROM current_node cn LEFT JOIN changeset cs 
ON cn.fk_changeset_id = cs.id
ORDER BY cn.id;
*/

/*
SELECT pjt.id AS project_id, cs.id AS changeset_id
FROM project pjt LEFT JOIN changeset cs ON pjt.id = cs.fk_project_id
WHERE pjt.id = 1001;


-- get the elements of the changesets of a specific project
SELECT changeset.project_id, element.fk_changeset_id, element.id, element.geom, element.visible
FROM 
(
    -- get the changesets of a specific project
    SELECT project.id AS project_id, changeset.id AS changeset_id
    FROM project LEFT JOIN changeset ON project.id = changeset.fk_project_id
    WHERE project.id = 1001
) AS changeset
LEFT JOIN current_area element ON changeset.changeset_id = element.fk_changeset_id
WHERE element.visible=TRUE;


SELECT element.id, element.geom, element.fk_changeset_id, element.visible
FROM current_node element LEFT JOIN changeset ON element.fk_changeset_id = changeset.id
WHERE changeset.id = 1001;
*/
             
