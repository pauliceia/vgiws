
-- Seg 11 Dez 2017 11:53:16 -02

-- -----------------------------------------------------
-- Table user_
-- -----------------------------------------------------
DROP TABLE IF EXISTS user_ CASCADE ;

CREATE TABLE IF NOT EXISTS user_ (
  id SERIAL ,
  username VARCHAR(45) NULL,
  email VARCHAR(45) NULL,
  password VARCHAR(45) NULL,
  is_email_valid BOOLEAN NULL,
  create_at TIMESTAMP NULL,
  removed_at TIMESTAMP NULL,
  terms_agreed TIMESTAMP NULL,
  terms_seen BOOLEAN NULL,
  PRIMARY KEY (id)
);


-- -----------------------------------------------------
-- Table layer
-- -----------------------------------------------------
DROP TABLE IF EXISTS layer CASCADE ;

CREATE TABLE IF NOT EXISTS layer (
  id SERIAL ,
  create_at TIMESTAMP NULL,
  removed_at TIMESTAMP NULL,
  visible BOOLEAN NULL DEFAULT TRUE,
  fk_user_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_project_user1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table changeset
-- -----------------------------------------------------
DROP TABLE IF EXISTS changeset CASCADE ;

CREATE TABLE IF NOT EXISTS changeset (
  id SERIAL ,
  create_at TIMESTAMP NULL,
  closed_at TIMESTAMP NULL,
  visible BOOLEAN NULL DEFAULT TRUE,
  fk_layer_id INT NOT NULL,
  fk_user_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_tb_project_tb_user1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_change_set_project1
    FOREIGN KEY (fk_layer_id)
    REFERENCES layer (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table point
-- -----------------------------------------------------
DROP TABLE IF EXISTS point CASCADE ;

CREATE TABLE IF NOT EXISTS point (
  id SERIAL ,
  geom GEOMETRY(MULTIPOINT, 4326) NULL,
  visible BOOLEAN NULL DEFAULT TRUE,
  version INT NOT NULL DEFAULT 1,
  fk_changeset_id INT NOT NULL,
  PRIMARY KEY (id, version),
  CONSTRAINT fk_tb_contribution_tb_project1
    FOREIGN KEY (fk_changeset_id)
    REFERENCES changeset (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table user_tag
-- -----------------------------------------------------
DROP TABLE IF EXISTS user_tag CASCADE ;

CREATE TABLE IF NOT EXISTS user_tag (
  id SERIAL ,
  k TEXT NOT NULL,
  v TEXT NULL,
  fk_user_id INT NOT NULL,
  PRIMARY KEY (id, k),
  CONSTRAINT fk_account_user1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table changeset_comment
-- -----------------------------------------------------
DROP TABLE IF EXISTS changeset_comment CASCADE ;

CREATE TABLE IF NOT EXISTS changeset_comment (
  id SERIAL ,
  body TEXT NULL,
  create_at TIMESTAMP NULL,
  visible BOOLEAN NULL DEFAULT TRUE,
  fk_changeset_id INT NOT NULL,
  fk_user_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_node_comment_change_group1
    FOREIGN KEY (fk_changeset_id)
    REFERENCES changeset (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_node_comment_user1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table line
-- -----------------------------------------------------
DROP TABLE IF EXISTS line CASCADE ;

CREATE TABLE IF NOT EXISTS line (
  id SERIAL ,
  geom GEOMETRY(MULTILINESTRING, 4326) NULL,
  visible BOOLEAN NULL DEFAULT TRUE,
  version INT NOT NULL DEFAULT 1,
  fk_changeset_id INT NOT NULL,
  PRIMARY KEY (id, version),
  CONSTRAINT fk_table1_changeset1
    FOREIGN KEY (fk_changeset_id)
    REFERENCES changeset (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table line_tag
-- -----------------------------------------------------
DROP TABLE IF EXISTS line_tag CASCADE ;
 

-- -----------------------------------------------------
-- Table point_tag
-- -----------------------------------------------------
DROP TABLE IF EXISTS point_tag CASCADE ;
 

-- -----------------------------------------------------
-- Table message
-- -----------------------------------------------------
DROP TABLE IF EXISTS message CASCADE ;

CREATE TABLE IF NOT EXISTS message (
  id SERIAL ,
  title TEXT NULL,
  body TEXT NULL,
  sent_on TIMESTAMP NULL,
  message_read BOOLEAN NULL,
  fk_user_id_from INT NOT NULL,
  fk_user_id_to INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_message_user1
    FOREIGN KEY (fk_user_id_from)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_message_user2
    FOREIGN KEY (fk_user_id_to)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table auth
-- -----------------------------------------------------
DROP TABLE IF EXISTS auth CASCADE ;

CREATE TABLE IF NOT EXISTS auth (
  id SERIAL ,
  is_admin BOOLEAN NULL DEFAULT FALSE,
  allow_import_bulk BOOLEAN NOT NULL DEFAULT FALSE,
  fk_user_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_auth_user1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table friend
-- -----------------------------------------------------
DROP TABLE IF EXISTS friend CASCADE ;

CREATE TABLE IF NOT EXISTS friend (
  fk_user_id INT NOT NULL,
  fk_user_id_friend INT NOT NULL,
  PRIMARY KEY (fk_user_id, fk_user_id_friend),
  CONSTRAINT fk_friend_user1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_friend_user2
    FOREIGN KEY (fk_user_id_friend)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table polygon
-- -----------------------------------------------------
DROP TABLE IF EXISTS polygon CASCADE ;

CREATE TABLE IF NOT EXISTS polygon (
  id SERIAL ,
  geom GEOMETRY(MULTIPOLYGON, 4326) NULL,
  visible BOOLEAN NULL DEFAULT TRUE,
  version INT NOT NULL DEFAULT 1,
  fk_changeset_id INT NOT NULL,
  PRIMARY KEY (id, version),
  CONSTRAINT fk_area_change_set1
    FOREIGN KEY (fk_changeset_id)
    REFERENCES changeset (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table polygon_tag
-- -----------------------------------------------------
DROP TABLE IF EXISTS polygon_tag CASCADE ;
 

-- -----------------------------------------------------
-- Table project
-- -----------------------------------------------------
DROP TABLE IF EXISTS project CASCADE ;

CREATE TABLE IF NOT EXISTS project (
  id SERIAL ,
  create_at TIMESTAMP NULL,
  removed_at TIMESTAMP NULL,
  visible BOOLEAN NULL DEFAULT TRUE,
  fk_user_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_project_user_1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table project_subscriber
-- -----------------------------------------------------
DROP TABLE IF EXISTS project_subscriber CASCADE ;

CREATE TABLE IF NOT EXISTS project_subscriber (
  fk_user_id INT NOT NULL,
  fk_project_id INT NOT NULL,
  permission VARCHAR(45) NULL,
  PRIMARY KEY (fk_user_id, fk_project_id),
  CONSTRAINT fk_project_subscriber_user1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_project_subscriber_project1
    FOREIGN KEY (fk_project_id)
    REFERENCES project (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table current_point
-- -----------------------------------------------------
DROP TABLE IF EXISTS current_point CASCADE ;

CREATE TABLE IF NOT EXISTS current_point (
  id SERIAL ,
  geom GEOMETRY(MULTIPOINT, 4326) NULL,
  visible BOOLEAN NULL DEFAULT TRUE,
  version INT NULL DEFAULT 1,
  fk_changeset_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_tb_contribution_tb_project10
    FOREIGN KEY (fk_changeset_id)
    REFERENCES changeset (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table current_polygon
-- -----------------------------------------------------
DROP TABLE IF EXISTS current_polygon CASCADE ;

CREATE TABLE IF NOT EXISTS current_polygon (
  id SERIAL ,
  geom GEOMETRY(MULTIPOLYGON, 4326) NULL,
  visible BOOLEAN NULL DEFAULT TRUE,
  version INT NULL DEFAULT 1,
  fk_changeset_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_area_change_set10
    FOREIGN KEY (fk_changeset_id)
    REFERENCES changeset (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table current_polygon_tag
-- -----------------------------------------------------
DROP TABLE IF EXISTS current_polygon_tag CASCADE ;
 

-- -----------------------------------------------------
-- Table current_line
-- -----------------------------------------------------
DROP TABLE IF EXISTS current_line CASCADE ;

CREATE TABLE IF NOT EXISTS current_line (
  id SERIAL ,
  geom GEOMETRY(MULTILINESTRING, 4326) NULL,
  visible BOOLEAN NULL DEFAULT TRUE,
  version INT NULL DEFAULT 1,
  fk_changeset_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_table1_changeset10
    FOREIGN KEY (fk_changeset_id)
    REFERENCES changeset (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table current_line_tag
-- -----------------------------------------------------
DROP TABLE IF EXISTS current_line_tag CASCADE ;
 

-- -----------------------------------------------------
-- Table current_point_tag
-- -----------------------------------------------------
DROP TABLE IF EXISTS current_point_tag CASCADE ;
 

-- -----------------------------------------------------
-- Table changeset_tag
-- -----------------------------------------------------
DROP TABLE IF EXISTS changeset_tag CASCADE ;

CREATE TABLE IF NOT EXISTS changeset_tag (
  id SERIAL ,
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NULL,
  fk_changeset_id INT NOT NULL,
  PRIMARY KEY (id, k),
  CONSTRAINT fk_way_tag_copy1_changeset1
    FOREIGN KEY (fk_changeset_id)
    REFERENCES changeset (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table layer_tag
-- -----------------------------------------------------
DROP TABLE IF EXISTS layer_tag CASCADE ;

CREATE TABLE IF NOT EXISTS layer_tag (
  id SERIAL ,
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NULL,
  fk_layer_id INT NOT NULL,
  PRIMARY KEY (id, k),
  CONSTRAINT fk_project_tag_project1
    FOREIGN KEY (fk_layer_id)
    REFERENCES layer (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table has
-- -----------------------------------------------------
DROP TABLE IF EXISTS has CASCADE ;

CREATE TABLE IF NOT EXISTS has (
  fk_project_id INT NOT NULL,
  fk_layer_id INT NOT NULL,
  PRIMARY KEY (fk_project_id, fk_layer_id),
  CONSTRAINT fk_has_project1
    FOREIGN KEY (fk_project_id)
    REFERENCES project (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_has_layer1
    FOREIGN KEY (fk_layer_id)
    REFERENCES layer (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table project_tag
-- -----------------------------------------------------
DROP TABLE IF EXISTS project_tag CASCADE ;

CREATE TABLE IF NOT EXISTS project_tag (
  id SERIAL ,
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NULL,
  fk_project_id INT NOT NULL,
  PRIMARY KEY (id, k),
  CONSTRAINT fk_project_project1
    FOREIGN KEY (fk_project_id)
    REFERENCES project (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table layer_subscriber
-- -----------------------------------------------------
DROP TABLE IF EXISTS layer_subscriber CASCADE ;

CREATE TABLE IF NOT EXISTS layer_subscriber (
  fk_layer_id INT NOT NULL,
  fk_user_id INT NOT NULL,
  permission INT NULL,
  PRIMARY KEY (fk_layer_id, fk_user_id),
  CONSTRAINT fk_layer_subscriber_layer1
    FOREIGN KEY (fk_layer_id)
    REFERENCES layer (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_layer_subscriber_user_1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Tables *_tag
-- -----------------------------------------------------
    
CREATE TABLE IF NOT EXISTS line_tag (
  id SERIAL ,
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NULL,
  version INT NOT NULL DEFAULT 1,  
  fk_line_id INT NOT NULL,
  fk_line_version INT NOT NULL,
  PRIMARY KEY (id, version, k),
  CONSTRAINT fk_line_tag_line1
    FOREIGN KEY (fk_line_id, fk_line_version)
    REFERENCES line (id, version)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS point_tag (
  id SERIAL ,
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NULL,
  version INT NOT NULL DEFAULT 1,
  fk_point_id INT NOT NULL,
  fk_point_version INT NOT NULL,
  PRIMARY KEY (id, version, k),
  CONSTRAINT fk_point_tag_point1
    FOREIGN KEY (fk_point_id, fk_point_version)
    REFERENCES point (id, version)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS polygon_tag (
  id SERIAL ,
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NULL,
  version INT NOT NULL DEFAULT 1,
  fk_polygon_id INT NOT NULL,
  fk_polygon_version INT NOT NULL,
  PRIMARY KEY (id, version, k),
  CONSTRAINT fk_polygon_tag_polygon1
    FOREIGN KEY (fk_polygon_id, fk_polygon_version)
    REFERENCES polygon (id, version)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS current_line_tag (
  id SERIAL ,
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NULL,
  fk_current_line_id INT NOT NULL,
  PRIMARY KEY (id, k),
  CONSTRAINT fk_current_line_tag_current_line1
    FOREIGN KEY (fk_current_line_id)
    REFERENCES current_line (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS current_point_tag (
  id SERIAL ,
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NULL,
  fk_current_point_id INT NOT NULL,
  PRIMARY KEY (id, k),
  CONSTRAINT fk_current_point_tag_current_point1
    FOREIGN KEY (fk_current_point_id)
    REFERENCES current_point (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS current_polygon_tag (
  id SERIAL ,
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NULL,
  fk_current_polygon_id INT NOT NULL,
  PRIMARY KEY (id, k),
  CONSTRAINT fk_current_polygon_tag_current_polygon1
    FOREIGN KEY (fk_current_polygon_id)
    REFERENCES current_polygon (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

