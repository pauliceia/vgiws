
-- -----------------------------------------------------
-- Table user
-- -----------------------------------------------------
-- clean user table
DELETE FROM user_;

-- add users
INSERT INTO user_ (id, username, email, password) VALUES (1001, 'admin', 'admin@admin.com', 'admin');
INSERT INTO user_ (id, username, email, password) VALUES (1002, 'rodrigo', 'rodrigo@admin.com', 'rodrigo');
INSERT INTO user_ (id, username, email, password) VALUES (1003, 'miguel', 'miguel@admin.com', 'miguel');
INSERT INTO user_ (id, username, email, password) VALUES (1004, 'rafael', 'rafael@admin.com', 'rafael');
INSERT INTO user_ (id, username, email, password) VALUES (1005, 'gabriel', 'gabriel@admin.com', 'gabriel');

SELECT * FROM user_;
-- SELECT id, username, name FROM user_ WHERE email='admin@admin.com';
-- SELECT id, username, name FROM user_ WHERE email='admin@admin.c';


-- -----------------------------------------------------
-- Table user_tag
-- -----------------------------------------------------
-- clean user_tag table
DELETE FROM user_tag;

-- insert values in table user_tag
-- user 1001
INSERT INTO user_tag (k, v, fk_user_id) VALUES ('name', 'Administrator', 1001);
INSERT INTO user_tag (k, v, fk_user_id) VALUES ('institution', 'INPE', 1001);
-- user 1002
INSERT INTO user_tag (k, v, fk_user_id) VALUES ('name', 'Rodrigo', 1002);
INSERT INTO user_tag (k, v, fk_user_id) VALUES ('institution', 'INPE', 1002);
-- user 1003
INSERT INTO user_tag (k, v, fk_user_id) VALUES ('name', 'Miguel', 1003);
-- user 1004
INSERT INTO user_tag (k, v, fk_user_id) VALUES ('name', 'Rafael', 1004);
-- user 1005
INSERT INTO user_tag (k, v, fk_user_id) VALUES ('name', 'Gabriel', 1005);



-- -----------------------------------------------------
-- Table auth
-- -----------------------------------------------------
-- clean auth table
DELETE FROM auth;

-- insert values in auth table
-- user 1001
INSERT INTO auth (id, is_admin, allow_import_bulk, fk_user_id) VALUES (1001, TRUE, TRUE, 1001);
-- user 1002
INSERT INTO auth (id, is_admin, allow_import_bulk, fk_user_id) VALUES (1002, TRUE, TRUE, 1002);



-- -----------------------------------------------------
-- Table notification
-- -----------------------------------------------------
-- clean notification table
DELETE FROM notification;

-- add notification
INSERT INTO notification (id, create_at, fk_user_id) VALUES (1001, '2017-01-01', 1001);
INSERT INTO notification (id, create_at, fk_user_id) VALUES (1002, '2017-03-25', 1001);
INSERT INTO notification (id, create_at, fk_user_id) VALUES (1003, '2017-12-25', 1002);
INSERT INTO notification (id, create_at, fk_user_id) VALUES (1004, '2017-05-13', 1003);
INSERT INTO notification (id, create_at, removed_at, fk_user_id, visible) VALUES (1005, '2017-08-15', '2017-10-25', 1003, FALSE);
INSERT INTO notification (id, create_at, removed_at, fk_user_id, visible) VALUES (1006, '2017-06-24', '2017-12-25', 1004, FALSE);



-- -----------------------------------------------------
-- Table notification_tag
-- -----------------------------------------------------
-- clean notification_tag table
DELETE FROM notification_tag;

-- insert values in table notification_tag
-- SOURCE: -
-- notification 1001
INSERT INTO notification_tag (k, v, fk_notification_id) VALUES ('body', 'Happy Birthday', 1001);
INSERT INTO notification_tag (k, v, fk_notification_id) VALUES ('url', '', 1001);
INSERT INTO notification_tag (k, v, fk_notification_id) VALUES ('type', 'birthday', 1001);  -- so the frontend, by the type, select a icon





-- -----------------------------------------------------
-- Table group_
-- -----------------------------------------------------
-- clean group_ table
DELETE FROM group_;

-- add group
INSERT INTO group_ (id, create_at, fk_user_id) VALUES (1001, '2017-01-01', 1001);
INSERT INTO group_ (id, create_at, fk_user_id) VALUES (1002, '2017-03-25', 1001);
INSERT INTO group_ (id, create_at, fk_user_id) VALUES (1003, '2017-12-25', 1002);
INSERT INTO group_ (id, create_at, fk_user_id) VALUES (1004, '2017-05-13', 1003);
INSERT INTO group_ (id, create_at, removed_at, fk_user_id, visible) VALUES (1005, '2017-08-15', '2017-10-25', 1003, FALSE);
INSERT INTO group_ (id, create_at, removed_at, fk_user_id, visible) VALUES (1006, '2017-06-24', '2017-12-25', 1004, FALSE);


-- -----------------------------------------------------
-- Table group_tag
-- -----------------------------------------------------
-- clean group_tag table
DELETE FROM group_tag;

-- insert values in table group_tag
-- SOURCE: -
-- project 1001
INSERT INTO group_tag (k, v, fk_group_id) VALUES ('name', 'Admins', 1001);
INSERT INTO group_tag (k, v, fk_group_id) VALUES ('description', 'Just admins', 1001);
-- project 1002
INSERT INTO group_tag (k, v, fk_group_id) VALUES ('name', 'INPE', 1002);
INSERT INTO group_tag (k, v, fk_group_id) VALUES ('description', '', 1002);
-- project 1003
INSERT INTO group_tag (k, v, fk_group_id) VALUES ('name', 'UNIFESP SJC', 1003);
INSERT INTO group_tag (k, v, fk_group_id) VALUES ('description', '', 1003);
-- project 1004
INSERT INTO group_tag (k, v, fk_group_id) VALUES ('name', 'UNIFESP Guarulhos', 1004);
INSERT INTO group_tag (k, v, fk_group_id) VALUES ('description', '', 1004);
-- project 1005
INSERT INTO group_tag (k, v, fk_group_id) VALUES ('name', 'Emory', 1005);
INSERT INTO group_tag (k, v, fk_group_id) VALUES ('description', '', 1005);
-- project 1006
INSERT INTO group_tag (k, v, fk_group_id) VALUES ('name', 'Arquivo Público do Estado de São Paulo', 1006);
INSERT INTO group_tag (k, v, fk_group_id) VALUES ('description', '', 1006);


-- -----------------------------------------------------
-- Table user_group
-- -----------------------------------------------------
-- clean user_group table
DELETE FROM user_group;

-- add user in a group
-- group 1001
INSERT INTO user_group (fk_group_id, fk_user_id, create_at) VALUES (1001, 1001, '2017-01-10');
INSERT INTO user_group (fk_group_id, fk_user_id, create_at) VALUES (1001, 1002, '2017-01-10');
-- group 1002
INSERT INTO user_group (fk_group_id, fk_user_id, create_at) VALUES (1002, 1002, '2017-01-10');
INSERT INTO user_group (fk_group_id, fk_user_id, create_at) VALUES (1002, 1003, '2017-01-10');
INSERT INTO user_group (fk_group_id, fk_user_id, create_at) VALUES (1002, 1004, '2017-01-10');
-- group 1003
INSERT INTO user_group (fk_group_id, fk_user_id, create_at) VALUES (1003, 1005, '2017-01-10');



-- -----------------------------------------------------
-- Table project
-- -----------------------------------------------------
-- clean project table
DELETE FROM project;

-- add layer
INSERT INTO project (id, create_at, fk_group_id, fk_user_id) VALUES (1001, '2017-11-20', 1001, 1001);
INSERT INTO project (id, create_at, fk_group_id, fk_user_id) VALUES (1002, '2017-10-12', 1001, 1002);
INSERT INTO project (id, create_at, fk_group_id, fk_user_id) VALUES (1003, '2017-12-23', 1002, 1002);
INSERT INTO project (id, create_at, fk_group_id, fk_user_id) VALUES (1004, '2017-09-11', 1002, 1004);
INSERT INTO project (id, create_at, fk_group_id, fk_user_id, visible) VALUES (1005, '2017-06-04', 1003, 1005, FALSE);

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
INSERT INTO project_tag (k, v, fk_project_id) VALUES ('name', 'admin', 1001);
INSERT INTO project_tag (k, v, fk_project_id) VALUES ('description', 'default project', 1001);
-- project 1002
INSERT INTO project_tag (k, v, fk_project_id) VALUES ('name', 'test project', 1002);
INSERT INTO project_tag (k, v, fk_project_id) VALUES ('url', 'http://somehost.com', 1002);
-- project 1003
INSERT INTO project_tag (k, v, fk_project_id) VALUES ('name', 'hello world', 1003);



-- -----------------------------------------------------
-- Table layer
-- -----------------------------------------------------
-- clean layer table
DELETE FROM layer;

-- add layer
INSERT INTO layer (id, create_at, fk_project_id, fk_user_id) VALUES (1001, '2017-11-20', 1001, 1001);
INSERT INTO layer (id, create_at, fk_project_id, fk_user_id) VALUES (1002, '2017-10-12', 1001, 1002);
INSERT INTO layer (id, create_at, fk_project_id, fk_user_id) VALUES (1003, '2017-12-23', 1002, 1002);
INSERT INTO layer (id, create_at, fk_project_id, fk_user_id) VALUES (1004, '2017-09-11', 1004, 1003);
INSERT INTO layer (id, create_at, fk_project_id, fk_user_id, visible) VALUES (1005, '2017-06-04', 1003, 1004, FALSE);

-- SELECT * FROM layer;
-- SELECT * FROM layer p WHERE p.id = 1001;


-- -----------------------------------------------------
-- Table layer_tag
-- -----------------------------------------------------
-- clean layer_tag table
DELETE FROM layer_tag;

-- insert values in table layer_tag
-- SOURCE: -
-- layer 1001
INSERT INTO layer_tag (k, v, fk_layer_id) VALUES ('name', 'default', 1001);
INSERT INTO layer_tag (k, v, fk_layer_id) VALUES ('description', 'default layer', 1001);
INSERT INTO layer_tag (k, v, fk_layer_id) VALUES ('theme', 'generic', 1001);
-- layer 1002
INSERT INTO layer_tag (k, v, fk_layer_id) VALUES ('name', 'test_layer', 1002);
INSERT INTO layer_tag (k, v, fk_layer_id) VALUES ('description', 'test_layer', 1002);
INSERT INTO layer_tag (k, v, fk_layer_id) VALUES ('theme', 'crime', 1002);
-- layer 1003
INSERT INTO layer_tag (k, v, fk_layer_id) VALUES ('name', 'layer 3', 1003);
INSERT INTO layer_tag (k, v, fk_layer_id) VALUES ('description', 'test_layer', 1003);
INSERT INTO layer_tag (k, v, fk_layer_id) VALUES ('theme', 'addresses', 1003);
-- layer 1004
INSERT INTO layer_tag (k, v, fk_layer_id) VALUES ('name', 'layer 4', 1004);
INSERT INTO layer_tag (k, v, fk_layer_id) VALUES ('description', 'test_layer', 1004);
-- layer layer_tag
INSERT INTO layer_tag (k, v, fk_layer_id) VALUES ('name', 'layer 5', 1005);
INSERT INTO layer_tag (k, v, fk_layer_id) VALUES ('description', 'test_layer', 1005);


-- SELECT * FROM layer_tag;

/*
SELECT p.id, p.create_at, p.removed_at FROM layer p WHERE p.id = 1003;
SELECT p.id, date(create_at) AS myTime, p.removed_at FROM layer p WHERE p.id = 1003;
SELECT p.id, to_char(create_at, 'YYYY-MM-DD HH24:MI:SS') as create_at, to_char(removed_at, 'YYYY-MM-DD HH24:MI:SS') as removed_at FROM layer p WHERE p.id = 1003;
*/

-- UPDATE layer SET visible = FALSE, removed_at=LOCALTIMESTAMP WHERE id=1001;


-- SELECT p.id, p.create_at, p.closed_at, ṕt.id, pt.k, pt.v FROM layer p, layer_tag pt WHERE p.id = pt.fk_layer_id;


/*
SELECT jsonb_build_object(
    'type', 'FeatureCollection',
    'features',   jsonb_agg(jsonb_build_object(
        'type',       'Layer',
        'properties', json_build_object(
            'id', id,
            'create_at',  to_char(create_at, 'YYYY-MM-DD HH24:MI:SS'),
            'removed_at', to_char(removed_at, 'YYYY-MM-DD HH24:MI:SS'),
            'fk_user_id_owner', fk_user_id_owner
        ),
        'tags',       tags.jsontags
    ))
) AS row_to_json
FROM layer
CROSS JOIN LATERAL (
	SELECT json_agg(json_build_object('k', k, 'v', v)) AS jsontags 
	FROM layer_tag 
	WHERE fk_layer_id = layer.id    
) AS tags
WHERE id=1001;
*/


-- -----------------------------------------------------
-- Table changeset
-- -----------------------------------------------------
-- clean changeset table
DELETE FROM changeset;

-- add changeset open
-- closed changesets (they will be closed in the final of file)
INSERT INTO changeset (id, create_at, fk_layer_id, fk_user_id) VALUES (1001, '2017-10-20', 1001, 1001);
INSERT INTO changeset (id, create_at, fk_layer_id, fk_user_id) VALUES (1002, '2017-11-10', 1002, 1002);
INSERT INTO changeset (id, create_at, fk_layer_id, fk_user_id) VALUES (1003, '2017-11-15', 1001, 1001);
INSERT INTO changeset (id, create_at, fk_layer_id, fk_user_id) VALUES (1004, '2017-01-20', 1002, 1002);
-- open changesets
INSERT INTO changeset (id, create_at, fk_layer_id, fk_user_id) VALUES (1005, '2017-03-25', 1003, 1003);
INSERT INTO changeset (id, create_at, fk_layer_id, fk_user_id) VALUES (1006, '2017-05-13', 1004, 1004);

-- SELECT * FROM changeset;


-- -----------------------------------------------------
-- Table changeset_tag
-- -----------------------------------------------------
-- clean changeset_tag table
DELETE FROM changeset_tag;

-- insert values in table changeset_tag
-- SOURCE: -
-- changeset 1001
INSERT INTO changeset_tag (k, v, fk_changeset_id) VALUES ('created_by', 'pauliceia_portal', 1001);
INSERT INTO changeset_tag (k, v, fk_changeset_id) VALUES ('comment', 'a changeset created', 1001);
-- changeset 1002
INSERT INTO changeset_tag (k, v, fk_changeset_id) VALUES ('created_by', 'test_postgresql', 1002);
INSERT INTO changeset_tag (k, v, fk_changeset_id) VALUES ('comment', 'changeset test', 1002);
-- changeset 1003
INSERT INTO changeset_tag (k, v, fk_changeset_id) VALUES ('created_by', 'pauliceia_portal', 1003);
INSERT INTO changeset_tag (k, v, fk_changeset_id) VALUES ('comment', 'a changeset created', 1003);
-- changeset 1004
INSERT INTO changeset_tag (k, v, fk_changeset_id) VALUES ('created_by', 'test_postgresql', 1004);
INSERT INTO changeset_tag (k, v, fk_changeset_id) VALUES ('comment', 'changeset test', 1004);

-- SELECT * FROM changeset_tag;

--SELECT c.id, c.create_at, c.closed_at, ct.id, ct.k, ct.v;
--FROM changeset c, changeset_tag ct WHERE c.id = ct.fk_changeset_id;



-- -----------------------------------------------------
-- Table current_point
-- -----------------------------------------------------
-- clean current_point table
DELETE FROM current_point;

-- add node
INSERT INTO current_point (id, geom, fk_changeset_id) VALUES (1001, ST_GeomFromText('MULTIPOINT((-23.546421 -46.635722))', 4326), 1001);
INSERT INTO current_point (id, geom, fk_changeset_id) VALUES (1002, ST_GeomFromText('MULTIPOINT((-23.55045 -46.634272))', 4326), 1002);
INSERT INTO current_point (id, geom, fk_changeset_id) VALUES (1003, ST_GeomFromText('MULTIPOINT((-23.542626 -46.638684))', 4326), 1003);
INSERT INTO current_point (id, geom, fk_changeset_id) VALUES (1004, ST_GeomFromText('MULTIPOINT((-23.547951 -46.634215))', 4326), 1004);
INSERT INTO current_point (id, geom, fk_changeset_id) VALUES (1005, ST_GeomFromText('MULTIPOINT((-23.530159 -46.654885))', 4326), 1001);
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
-- Table current_point_tag
-- -----------------------------------------------------
-- clean current_point_tag table
DELETE FROM current_point_tag;

-- insert values in table current_point_tag
-- SOURCE: AialaLevy_theaters20170710.xlsx
-- node 1001
INSERT INTO current_point_tag (k, v, fk_current_point_id) VALUES ('address', 'R. São José', 1001);
INSERT INTO current_point_tag (k, v, fk_current_point_id) VALUES ('start_date', '1869', 1001);
INSERT INTO current_point_tag (k, v, fk_current_point_id) VALUES ('end_date', '1869', 1001);
-- node 1002
INSERT INTO current_point_tag (k, v, fk_current_point_id) VALUES ('address', 'R. Marechal Deodoro', 1002);
INSERT INTO current_point_tag (k, v, fk_current_point_id) VALUES ('start_date', '1878', 1002);
INSERT INTO current_point_tag (k, v, fk_current_point_id) VALUES ('end_date', '1910', 1002);
-- node 1003
INSERT INTO current_point_tag (k, v, fk_current_point_id) VALUES ('address', 'R. 11 de Junho, 9 = D. José de Barros', 1003);
INSERT INTO current_point_tag (k, v, fk_current_point_id) VALUES ('start_date', '1886', 1003);
INSERT INTO current_point_tag (k, v, fk_current_point_id) VALUES ('end_date', '1916', 1003);
-- node 1004
INSERT INTO current_point_tag (k, v, fk_current_point_id) VALUES ('address', 'R. 15 de Novembro, 17A', 1004);
INSERT INTO current_point_tag (k, v, fk_current_point_id) VALUES ('start_date', '1890', 1004);
INSERT INTO current_point_tag (k, v, fk_current_point_id) VALUES ('end_date', '1911', 1004);
-- node 1005
INSERT INTO current_point_tag (k, v, fk_current_point_id) VALUES ('address', 'R. Barra Funda, 74', 1005);
INSERT INTO current_point_tag (k, v, fk_current_point_id) VALUES ('start_date', '1897', 1005);
INSERT INTO current_point_tag (k, v, fk_current_point_id) VALUES ('end_date', '1897', 1005);


-- -----------------------------------------------------
-- Operations with current_node
-- -----------------------------------------------------

-- SELECT * FROM current_node n WHERE visible=TRUE;

-- get just the valid nodes
-- SELECT n.id, ST_AsText(n.geom) as geom, n.version, n.fk_changeset_id, n.visible FROM current_node n WHERE visible=TRUE;

-- SELECT n.id, ST_AsText(n.geom) as geom, n.version, n.fk_changeset_id, nt.id, nt.k, nt.v FROM current_node n, node_tag nt WHERE n.id = nt.fk_node_id;

--SELECT * FROM current_node_tag;

-- "remove" some nodes
UPDATE current_point SET visible = FALSE WHERE id>=1003 AND id<=1005;






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
-- Table current_line
-- -----------------------------------------------------
-- clean current_line table
DELETE FROM current_line;

-- add way
INSERT INTO current_line (id, geom, fk_changeset_id) VALUES (1001, ST_GeomFromText('MULTILINESTRING((333188.261004703 7395284.32488995,333205.817689791 7395247.71277836,333247.996555184 7395172.56160195,333261.133400433 7395102.3470075,333270.981533908 7395034.48052247,333277.885095545 7394986.25678192))', 4326), 1001);
INSERT INTO current_line (id, geom, fk_changeset_id) VALUES (1002, ST_GeomFromText('MULTILINESTRING((333270.653184563 7395036.74327773,333244.47769325 7395033.35326418,333204.141105934 7395028.41654752,333182.467715735 7395026.2492085))', 4326), 1002);
INSERT INTO current_line (id, geom, fk_changeset_id) VALUES (1003, ST_GeomFromText('MULTILINESTRING((333175.973956142 7395098.49130924,333188.494819187 7395102.10309665,333248.637266893 7395169.13708777))', 4326), 1003);
INSERT INTO current_line (id, geom, fk_changeset_id) VALUES (1004, ST_GeomFromText('MULTILINESTRING((333247.996555184 7395172.56160195,333255.762310051 7395178.46616912,333307.926051785 7395235.76603312,333354.472159794 7395273.32392717))', 4326), 1004);
INSERT INTO current_line (id, geom, fk_changeset_id) VALUES (1005, ST_GeomFromText('MULTILINESTRING((333266.034554577 7395292.9053933,333308.06080675 7395235.87476644))', 4326), 1002);
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
-- Table current_line_tag
-- -----------------------------------------------------
-- clean current_line_tag table
DELETE FROM current_line_tag;

-- insert values in table current_line_tag
-- SOURCE: db_pauliceia
-- way 1
INSERT INTO current_line_tag (k, v, fk_current_line_id) VALUES ('name', 'rua boa vista', 1001);
INSERT INTO current_line_tag (k, v, fk_current_line_id) VALUES ('start_date', '1930', 1001);
INSERT INTO current_line_tag (k, v, fk_current_line_id) VALUES ('end_date', '1930', 1001);
-- way 2
INSERT INTO current_line_tag (k, v, fk_current_line_id) VALUES ('address', 'rua tres de dezembro', 1002);
INSERT INTO current_line_tag (k, v, fk_current_line_id) VALUES ('start_date', '1930', 1002);
INSERT INTO current_line_tag (k, v, fk_current_line_id) VALUES ('end_date', '1930', 1002);
-- way 3
INSERT INTO current_line_tag (k, v, fk_current_line_id) VALUES ('address', 'rua joao briccola', 1003);
INSERT INTO current_line_tag (k, v, fk_current_line_id) VALUES ('start_date', '1930', 1003);
INSERT INTO current_line_tag (k, v, fk_current_line_id) VALUES ('end_date', '1930', 1003);
-- way 4
INSERT INTO current_line_tag (k, v, fk_current_line_id) VALUES ('address', 'ladeira porto geral', 1004);
INSERT INTO current_line_tag (k, v, fk_current_line_id) VALUES ('start_date', '1930', 1004);
INSERT INTO current_line_tag (k, v, fk_current_line_id) VALUES ('end_date', '1930', 1004);
-- way 5
INSERT INTO current_line_tag (k, v, fk_current_line_id) VALUES ('address', 'travessa porto geral', 1005);
INSERT INTO current_line_tag (k, v, fk_current_line_id) VALUES ('start_date', '1930', 1005);
INSERT INTO current_line_tag (k, v, fk_current_line_id) VALUES ('end_date', '1930', 1005);


-- -----------------------------------------------------
-- Operations with current_way
-- -----------------------------------------------------

-- get just the valid nodes
-- SELECT id, geom, visible, version, fk_changeset_id FROM current_way WHERE visible=TRUE;

-- SELECT id, ST_AsText(geom) as geom, version, fk_changeset_id FROM way;
-- SELECT w.id, ST_AsText(w.geom) as geom, w.version, w.fk_changeset_id, wt.id, wt.k, wt.v FROM way w, way_tag wt WHERE w.id = wt.fk_way_id;

-- "remove" some lines
UPDATE current_line SET visible = FALSE WHERE id>=1003 AND id<=1007;

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
-- Table current_polygon
-- -----------------------------------------------------
-- clean current_polygon table
DELETE FROM current_polygon;

-- add area
INSERT INTO current_polygon (id, geom, fk_changeset_id) VALUES (1001, ST_GeomFromText('MULTIPOLYGON(((0 0, 1 1, 2 2, 3 3, 0 0)))', 4326), 1001);
INSERT INTO current_polygon (id, geom, fk_changeset_id) VALUES (1002, ST_GeomFromText('MULTIPOLYGON(((2 2, 3 3, 4 4, 5 5, 2 2)))', 4326), 1002);
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
-- Table current_polygon_tag
-- -----------------------------------------------------
-- clean current_polygon_tag table
DELETE FROM current_polygon_tag;

-- insert values in table current_polygon_tag
-- SOURCE: -
-- area 1
INSERT INTO current_polygon_tag (k, v, fk_current_polygon_id) VALUES ('building', 'hotel', 1001);
INSERT INTO current_polygon_tag (k, v, fk_current_polygon_id) VALUES ('start_date', '1870', 1001);
INSERT INTO current_polygon_tag (k, v, fk_current_polygon_id) VALUES ('end_date', '1900', 1001);
-- area 2
INSERT INTO current_polygon_tag (k, v, fk_current_polygon_id) VALUES ('building', 'theater', 1002);
INSERT INTO current_polygon_tag (k, v, fk_current_polygon_id) VALUES ('start_date', '1920', 1002);
INSERT INTO current_polygon_tag (k, v, fk_current_polygon_id) VALUES ('end_date', '1930', 1002);


-- -----------------------------------------------------
-- Operations with current_area
-- -----------------------------------------------------

-- get just the valid nodes
-- SELECT id, geom, visible, version, fk_changeset_id FROM current_area WHERE visible=TRUE;

-- SELECT id, ST_AsText(geom) as geom, version, fk_changeset_id FROM area;
-- SELECT a.id, ST_AsText(a.geom) as geom, a.version, a.fk_changeset_id, at.id, at.k, at.v FROM area a, area_tag at WHERE a.id = at.fk_area_id;

-- "remove" some areas
UPDATE current_polygon SET visible = FALSE WHERE id>=1006 AND id<=1007;





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
UPDATE changeset SET closed_at = '2017-12-01' WHERE id>=1001 AND id<=1004;




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
SELECT pjt.id AS layer_id, cs.id AS changeset_id
FROM layer pjt LEFT JOIN changeset cs ON pjt.id = cs.fk_layer_id
WHERE pjt.id = 1001;


-- get the elements of the changesets of a specific layer
SELECT changeset.layer_id, element.fk_changeset_id, element.id, element.geom, element.visible
FROM 
(
    -- get the changesets of a specific layer
    SELECT layer.id AS layer_id, changeset.id AS changeset_id
    FROM layer LEFT JOIN changeset ON layer.id = changeset.fk_layer_id
    WHERE layer.id = 1001
) AS changeset
LEFT JOIN current_area element ON changeset.changeset_id = element.fk_changeset_id
WHERE element.visible=TRUE;


SELECT element.id, element.geom, element.fk_changeset_id, element.visible
FROM current_node element LEFT JOIN changeset ON element.fk_changeset_id = changeset.id
WHERE changeset.id = 1001;
*/
