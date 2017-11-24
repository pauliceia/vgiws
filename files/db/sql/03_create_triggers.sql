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
            RAISE EXCEPTION 'The changeset with id=% is closed, so it is not possible to use it', NEW.fk_changeset_id;
        END IF;
        
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

-- Create a trigger to observe each current_element table when add a new element
CREATE TRIGGER trigger_observe_when_add_new_element_in_current_node_table BEFORE INSERT OR UPDATE ON current_node
    FOR EACH ROW EXECUTE PROCEDURE observe_when_add_new_element_in_current_element_table();

CREATE TRIGGER trigger_observe_when_add_new_element_in_current_way_table BEFORE INSERT OR UPDATE ON current_way
    FOR EACH ROW EXECUTE PROCEDURE observe_when_add_new_element_in_current_element_table();

CREATE TRIGGER trigger_observe_when_add_new_element_in_current_area_table BEFORE INSERT OR UPDATE ON current_area
    FOR EACH ROW EXECUTE PROCEDURE observe_when_add_new_element_in_current_element_table();


/*
INSERT INTO current_node (geom, fk_changeset_id) VALUES (ST_GeomFromText('MULTIPOINT((-23.530159 -46.654885))', 4326), 1003);
INSERT INTO current_way (geom, fk_changeset_id) VALUES (ST_GeomFromText('MULTILINESTRING((333188.261004703 7395284.32488995,333277.885095545 7394986.25678192))', 4326), 1003);
INSERT INTO current_area (geom, fk_changeset_id) VALUES (ST_GeomFromText('MULTIPOLYGON(((2 2, 3 3, 4 4, 5 5, 2 2)))', 4326), 1003);

SELECT closed_at FROM changeset WHERE changeset.id = 1003;
*/
