/*
VGI WS Errors:

VW001 - The changeset with id=#ID was closed at #CLOSED_AT, so it is not possible to use it

*/

-- -----------------------------------------------------
-- Triggers to current_element table
-- -----------------------------------------------------
-- create a generic function to observe when add a new element in current_element table
DROP FUNCTION IF EXISTS observe_when_add_new_element_in_current_element_table() CASCADE;

CREATE OR REPLACE FUNCTION observe_when_add_new_element_in_current_element_table() RETURNS trigger AS $$
    DECLARE
    __closed_at__ TIMESTAMP;
    BEGIN
        -- do a select looking for the changeset with same id of the changeset used to insert new element        
        __closed_at__ := (SELECT closed_at FROM changeset WHERE changeset.id = NEW.fk_changeset_id);

        -- if this changeset is closed (not null), so raise a exception
        IF __closed_at__ is not NULL THEN
            RAISE 'The changeset with id=% was closed at %, so it is not possible to use it.', NEW.fk_changeset_id, __closed_at__ 
                USING ERRCODE = 'VW001';
        END IF;
        
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

-- Create a trigger to observe each current_element table when add a new element
CREATE TRIGGER trigger_observe_when_add_new_element_in_current_point_table BEFORE INSERT OR UPDATE ON current_point
    FOR EACH ROW EXECUTE PROCEDURE observe_when_add_new_element_in_current_element_table();

CREATE TRIGGER trigger_observe_when_add_new_element_in_current_line_table BEFORE INSERT OR UPDATE ON current_line
    FOR EACH ROW EXECUTE PROCEDURE observe_when_add_new_element_in_current_element_table();

CREATE TRIGGER trigger_observe_when_add_new_element_in_current_polygon_table BEFORE INSERT OR UPDATE ON current_polygon
    FOR EACH ROW EXECUTE PROCEDURE observe_when_add_new_element_in_current_element_table();


/*
INSERT INTO current_node (geom, fk_changeset_id) VALUES (ST_GeomFromText('MULTIPOINT((-23.530159 -46.654885))', 4326), 1003);
INSERT INTO current_way (geom, fk_changeset_id) VALUES (ST_GeomFromText('MULTILINESTRING((333188.261004703 7395284.32488995,333277.885095545 7394986.25678192))', 4326), 1003);
INSERT INTO current_area (geom, fk_changeset_id) VALUES (ST_GeomFromText('MULTIPOLYGON(((2 2, 3 3, 4 4, 5 5, 2 2)))', 4326), 1003);

SELECT closed_at FROM changeset WHERE changeset.id = 1003;
*/


-- -----------------------------------------------------
-- Triggers to user_group table
-- -----------------------------------------------------
-- create a function to observe when add or update a new user in a group, if it can receive notifications, 
-- so put it as watchers of the projects of a group
DROP FUNCTION IF EXISTS observe_when_add_or_update_user_in_group_put_the_user_as_watchers_of_projects() CASCADE;

CREATE OR REPLACE FUNCTION observe_when_add_or_update_user_in_group_put_the_user_as_watchers_of_projects() RETURNS trigger AS $$
    DECLARE
        field RECORD;
    BEGIN

        RAISE NOTICE '';
        RAISE NOTICE '';
        RAISE NOTICE 'NEW.fk_group_id % - NEW.fk_user_id % - NEW.added_at %', NEW.fk_group_id, NEW.fk_user_id, NEW.added_at;
        RAISE NOTICE 'NEW.group_permission % - NEW.can_receive_notification % - NEW.fk_user_id_added_by %', NEW.group_permission, NEW.can_receive_notification, NEW.fk_user_id_added_by;
        

        -- create a temporary table (like a 'table variable') with the projects of a group
        CREATE TEMP TABLE projects_by_group ON COMMIT DROP AS
            SELECT id as project_id, fk_group_id as group_id FROM project WHERE project.fk_group_id = NEW.fk_group_id;

        -- if the user can receive notification
        IF NEW.can_receive_notification THEN

            -- print the projects of a group
            RAISE NOTICE '>>> Projects of the group %', NEW.fk_group_id;
            FOR field IN SELECT * FROM projects_by_group LOOP
                RAISE NOTICE 'project_id: %, group_id: %', field.project_id, field.group_id;
            END LOOP;

            -- insert the user as watcher of the projects that is inside a group
            FOR field IN SELECT * FROM projects_by_group LOOP
                INSERT INTO project_watcher (fk_project_id, fk_user_id) 
                    VALUES (field.project_id, NEW.fk_user_id)
                    -- if the pair project_id and user_id already exist, do nothing
                    ON CONFLICT (fk_project_id, fk_user_id) DO NOTHING;
            END LOOP;

            -- print the projects that the user is now watcher of a group
            RAISE NOTICE '>>> Projects that the user % is now a watcher', NEW.fk_user_id;
            FOR field IN SELECT * FROM project_watcher WHERE fk_user_id = NEW.fk_user_id LOOP
                RAISE NOTICE 'fk_project_id: %, fk_user_id: %', field.fk_project_id, field.fk_user_id;
            END LOOP;

        -- IF USER can NOT receive_notification THEN
        ELSE

            CREATE TEMP TABLE projects_that_user_is_watcher_from_group ON COMMIT DROP AS
                SELECT project_id, group_id, fk_user_id as user_id
                FROM projects_by_group AS pg LEFT JOIN project_watcher AS pw ON pg.project_id = pw.fk_project_id
                WHERE fk_user_id = user_id;

            -- print the lines of the table
            FOR field IN SELECT * FROM projects_that_user_is_watcher_from_group LOOP
                RAISE NOTICE 'project_id: %s, group_id: %s, user_id: %s', field.project_id, field.group_id, field.user_id;
            END LOOP;   


            -- remove the temp tables
            DROP TABLE projects_that_user_is_watcher_from_group CASCADE;     

        END IF;

        -- remove the temp table
        DROP TABLE projects_by_group CASCADE;
                
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_observe_when_add_or_update_user_in_group_put_the_user_as_watchers_of_projects BEFORE INSERT OR UPDATE ON user_group
    FOR EACH ROW EXECUTE PROCEDURE observe_when_add_or_update_user_in_group_put_the_user_as_watchers_of_projects();





-- TESTS

DELETE FROM project_watcher;

SELECT * FROM project_watcher
WHERE fk_user_id = 1001;

-- -----------------------------------------------------
-- Table user_group
-- -----------------------------------------------------
-- clean user_group table
DELETE FROM user_group;

-- add user in a group
-- group 1001
INSERT INTO user_group (fk_group_id, fk_user_id, added_at, group_permission, fk_user_id_added_by) VALUES (1001, 1001, '2017-01-01', 'admin', 1001);
INSERT INTO user_group (fk_group_id, fk_user_id, added_at, group_permission, fk_user_id_added_by) VALUES (1001, 1002, '2017-03-25', 'admin', 1001);
-- group 1002
INSERT INTO user_group (fk_group_id, fk_user_id, added_at, group_permission, fk_user_id_added_by) VALUES (1002, 1001, '2017-05-13', 'admin', 1001);
INSERT INTO user_group (fk_group_id, fk_user_id, added_at, group_permission, fk_user_id_added_by) VALUES (1002, 1002, '2017-06-13', 'admin', 1001);
INSERT INTO user_group (fk_group_id, fk_user_id, added_at, can_receive_notification, fk_user_id_added_by) VALUES (1002, 1003, '2017-08-15', FALSE, 1001);
INSERT INTO user_group (fk_group_id, fk_user_id, added_at, fk_user_id_added_by) VALUES (1002, 1004, '2017-12-08', 1002);
-- group 1003
INSERT INTO user_group (fk_group_id, fk_user_id, added_at, group_permission, fk_user_id_added_by) 
VALUES (1003, 1002, '2017-12-12', 'admin', 1002);
INSERT INTO user_group (fk_group_id, fk_user_id, added_at, can_receive_notification, fk_user_id_added_by) 
VALUES (1003, 1003, '2017-12-15', FALSE, 1002);
-- group 1004
INSERT INTO user_group (fk_group_id, fk_user_id, added_at, group_permission, fk_user_id_added_by) 
VALUES (1004, 1003, '2017-01-11', 'admin', 1003);
INSERT INTO user_group (fk_group_id, fk_user_id, added_at, group_permission, fk_user_id_added_by) 
VALUES (1004, 1004, '2017-05-02', 'admin', 1003);
INSERT INTO user_group (fk_group_id, fk_user_id, added_at, can_receive_notification, fk_user_id_added_by) 
VALUES (1004, 1001, '2017-06-15', FALSE, 1004);
INSERT INTO user_group (fk_group_id, fk_user_id, added_at, can_receive_notification, fk_user_id_added_by) 
VALUES (1004, 1002, '2017-12-19', FALSE, 1004);
INSERT INTO user_group (fk_group_id, fk_user_id, added_at, fk_user_id_added_by) 
VALUES (1004, 1005, '2017-12-20', 1004);
-- group 1005
INSERT INTO user_group (fk_group_id, fk_user_id, added_at, group_permission, fk_user_id_added_by) 
VALUES (1005, 1003, '2017-01-10', 'admin', 1003);
-- group 1006
INSERT INTO user_group (fk_group_id, fk_user_id, added_at, group_permission, fk_user_id_added_by) 
VALUES (1006, 1004, '2017-01-10', 'admin', 1004);




