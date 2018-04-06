-- https://coderwall.com/p/whf3-a/hierarchical-data-in-postgres

/*
DROP TABLE IF EXISTS section;

CREATE TABLE section (
    id INTEGER PRIMARY KEY,
    name TEXT,
    parent_id INTEGER REFERENCES section
);

--ALTER TABLE page ADD COLUMN parent_id INTEGER REFERENCES page;
CREATE INDEX section_parent_id_idx ON section (parent_id);

INSERT INTO section (id, name, parent_id) VALUES (1, 'Section A', NULL);
INSERT INTO section (id, name, parent_id) VALUES (2, 'Section A.1', 1);
INSERT INTO section (id, name, parent_id) VALUES (3, 'Section B', NULL);
INSERT INTO section (id, name, parent_id) VALUES (4, 'Section B.1', 3);
INSERT INTO section (id, name, parent_id) VALUES (5, 'Section B.2', 3);
INSERT INTO section (id, name, parent_id) VALUES (6, 'Section B.2.1', 5);

SELECT * FROM section WHERE id = 3 OR parent_id = 3;



WITH RECURSIVE nodes(id,name,parent_id) AS (
    SELECT s1.id, s1.name, s1.parent_id
    FROM section s1 WHERE parent_id = 3
        UNION
    SELECT s2.id, s2.name, s2.parent_id
    FROM section s2, nodes s1 WHERE s2.parent_id = s1.id
)
SELECT * FROM nodes;
*/



-- CREATE EXTENSION ltree;

/*
DROP TABLE IF EXISTS section;

CREATE TABLE section (
    id INTEGER PRIMARY KEY,
    name TEXT,
    parent_path LTREE
);

CREATE INDEX section_parent_path_idx ON section USING GIST (parent_path);


INSERT INTO section (id, name, parent_path) VALUES (1, 'Section 1', 'root');
INSERT INTO section (id, name, parent_path) VALUES (2, 'Section 1.1', 'root.1');
INSERT INTO section (id, name, parent_path) VALUES (3, 'Section 2', 'root');
INSERT INTO section (id, name, parent_path) VALUES (4, 'Section 2.1', 'root.3');
INSERT INTO section (id, name, parent_path) VALUES (5, 'Section 2.2', 'root.3');
INSERT INTO section (id, name, parent_path) VALUES (6, 'Section 2.2.1', 'root.3.5');


SELECT * FROM section WHERE parent_path <@ 'root.3';
*/


DROP TABLE IF EXISTS section;

CREATE TABLE section (
    id INTEGER PRIMARY KEY,
    name TEXT,
    parent_id INTEGER REFERENCES section,
    parent_path LTREE
);

CREATE INDEX section_parent_path_idx ON section USING GIST (parent_path);
CREATE INDEX section_parent_id_idx ON section (parent_id);

CREATE OR REPLACE FUNCTION update_section_parent_path() RETURNS TRIGGER AS $$
    DECLARE
        path ltree;
    BEGIN
        IF NEW.parent_id IS NULL THEN
            NEW.parent_path = 'root'::ltree;
        ELSEIF TG_OP = 'INSERT' OR OLD.parent_id IS NULL OR OLD.parent_id != NEW.parent_id THEN
            SELECT parent_path || id::text FROM section WHERE id = NEW.parent_id INTO path;
            IF path IS NULL THEN
                RAISE EXCEPTION 'Invalid parent_id %', NEW.parent_id;
            END IF;
            NEW.parent_path = path;
        END IF;
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER parent_path_tgr
    BEFORE INSERT OR UPDATE ON section
    FOR EACH ROW EXECUTE PROCEDURE update_section_parent_path();



-- https://coderwall.com/p/z00-yw/use-ltreee-plv8-to-fetch-hirarcical-records-as-json

-- CREATE EXTENSION ltree;
CREATE EXTENSION plv8;











