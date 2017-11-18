

-- -----------------------------------------------------
-- Table user_
-- -----------------------------------------------------
DROP TABLE IF EXISTS user_ CASCADE ;

CREATE TABLE IF NOT EXISTS user_ (
  id SERIAL ,
  username VARCHAR(45) NULL,
  email VARCHAR(45) NULL,
  password VARCHAR(45) NULL,
  name VARCHAR(50) NULL,
  is_email_valid BOOLEAN NULL,
  description TEXT NULL,
  create_at TIMESTAMP NULL,
  removed_at TIMESTAMP NULL,
  terms_agreed TIMESTAMP NULL,
  terms_seen BOOLEAN NULL,
  PRIMARY KEY (id)
);


-- -----------------------------------------------------
-- Table project
-- -----------------------------------------------------
DROP TABLE IF EXISTS project CASCADE ;

CREATE TABLE IF NOT EXISTS project (
  id SERIAL ,
  create_at TIMESTAMP NULL,
  removed_at TIMESTAMP NULL,
  visible BOOLEAN NULL DEFAULT TRUE,
  fk_user_id_owner INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_project_user1
    FOREIGN KEY (fk_user_id_owner)
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
  fk_project_id INT NOT NULL,
  fk_user_id_owner INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_tb_project_tb_user1
    FOREIGN KEY (fk_user_id_owner)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_change_set_project1
    FOREIGN KEY (fk_project_id)
    REFERENCES project (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table node
-- -----------------------------------------------------
DROP TABLE IF EXISTS node CASCADE ;

CREATE TABLE IF NOT EXISTS node (
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
-- Table user_preference
-- -----------------------------------------------------
DROP TABLE IF EXISTS user_preference CASCADE ;

CREATE TABLE IF NOT EXISTS user_preference (
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
  fk_user_id_author INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_node_comment_change_group1
    FOREIGN KEY (fk_changeset_id)
    REFERENCES changeset (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_node_comment_user1
    FOREIGN KEY (fk_user_id_author)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table way
-- -----------------------------------------------------
DROP TABLE IF EXISTS way CASCADE ;

CREATE TABLE IF NOT EXISTS way (
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
-- Table way_tag
-- -----------------------------------------------------
DROP TABLE IF EXISTS way_tag CASCADE ;
 

-- -----------------------------------------------------
-- Table node_tag
-- -----------------------------------------------------
DROP TABLE IF EXISTS node_tag CASCADE ;
 

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
  allow_import_bulk BOOLEAN NOT NULL,
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
-- Table area
-- -----------------------------------------------------
DROP TABLE IF EXISTS area CASCADE ;

CREATE TABLE IF NOT EXISTS area (
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
-- Table area_tag
-- -----------------------------------------------------
DROP TABLE IF EXISTS area_tag CASCADE ;
 

-- -----------------------------------------------------
-- Table project_subscriber
-- -----------------------------------------------------
DROP TABLE IF EXISTS project_subscriber CASCADE ;

CREATE TABLE IF NOT EXISTS project_subscriber (
  permission VARCHAR(45) NULL,
  fk_id_user INT NOT NULL,
  fk_id_project INT NOT NULL,
  PRIMARY KEY (fk_id_user, fk_id_project),
  CONSTRAINT fk_project_subscriber_user1
    FOREIGN KEY (fk_id_user)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_project_subscriber_project1
    FOREIGN KEY (fk_id_project)
    REFERENCES project (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table current_node
-- -----------------------------------------------------
DROP TABLE IF EXISTS current_node CASCADE ;

CREATE TABLE IF NOT EXISTS current_node (
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
-- Table current_area
-- -----------------------------------------------------
DROP TABLE IF EXISTS current_area CASCADE ;

CREATE TABLE IF NOT EXISTS current_area (
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
-- Table current_area_tag
-- -----------------------------------------------------
DROP TABLE IF EXISTS current_area_tag CASCADE ;
 

-- -----------------------------------------------------
-- Table current_way
-- -----------------------------------------------------
DROP TABLE IF EXISTS current_way CASCADE ;

CREATE TABLE IF NOT EXISTS current_way (
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
-- Table current_way_tag
-- -----------------------------------------------------
DROP TABLE IF EXISTS current_way_tag CASCADE ;
 

-- -----------------------------------------------------
-- Table current_node_tag
-- -----------------------------------------------------
DROP TABLE IF EXISTS current_node_tag CASCADE ;
 

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
-- Table project_tag
-- -----------------------------------------------------
DROP TABLE IF EXISTS project_tag CASCADE ;

CREATE TABLE IF NOT EXISTS project_tag (
  id SERIAL ,
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NULL,
  fk_project_id INT NOT NULL,
  PRIMARY KEY (id, k),
  CONSTRAINT fk_project_tag_project1
    FOREIGN KEY (fk_project_id)
    REFERENCES project (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Tables *_tag
-- -----------------------------------------------------
    
CREATE TABLE IF NOT EXISTS way_tag (
  id SERIAL ,
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NULL,
  version INT NOT NULL DEFAULT 1,  
  fk_way_id INT NOT NULL,
  fk_way_version INT NOT NULL,
  PRIMARY KEY (id, version, k),
  CONSTRAINT fk_way_tag_way1
    FOREIGN KEY (fk_way_id, fk_way_version)
    REFERENCES way (id, version)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS node_tag (
  id SERIAL ,
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NULL,
  version INT NOT NULL DEFAULT 1,
  fk_node_id INT NOT NULL,
  fk_node_version INT NOT NULL,
  PRIMARY KEY (id, version, k),
  CONSTRAINT fk_node_tag_node1
    FOREIGN KEY (fk_node_id, fk_node_version)
    REFERENCES node (id, version)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS area_tag (
  id SERIAL ,
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NULL,
  version INT NOT NULL DEFAULT 1,
  fk_area_id INT NOT NULL,
  fk_area_version INT NOT NULL,
  PRIMARY KEY (id, version, k),
  CONSTRAINT fk_area_tag_area1
    FOREIGN KEY (fk_area_id, fk_area_version)
    REFERENCES area (id, version)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS current_way_tag (
  id SERIAL ,
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NULL,
  fk_current_way_id INT NOT NULL,
  PRIMARY KEY (id, k),
  CONSTRAINT fk_current_way_tag_current_way1
    FOREIGN KEY (fk_current_way_id)
    REFERENCES current_way (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS current_node_tag (
  id SERIAL ,
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NULL,
  fk_current_node_id INT NOT NULL,
  PRIMARY KEY (id, k),
  CONSTRAINT fk_current_node_tag_current_node1
    FOREIGN KEY (fk_current_node_id)
    REFERENCES current_node (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS current_area_tag (
  id SERIAL ,
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NULL,
  fk_current_area_id INT NOT NULL,
  PRIMARY KEY (id, k),
  CONSTRAINT fk_current_area_tag_current_area1
    FOREIGN KEY (fk_current_area_id)
    REFERENCES current_area (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

