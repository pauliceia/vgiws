
-- Ter 24 Abr 2018 17:54:12 -03

-- -----------------------------------------------------
-- Table user_
-- -----------------------------------------------------
DROP TABLE IF EXISTS user_ CASCADE ;

CREATE TABLE IF NOT EXISTS user_ (
  id SERIAL ,
  email TEXT NOT NULL,
  password TEXT NOT NULL,
  username TEXT NOT NULL,
  name TEXT NULL,
  created_at TIMESTAMP NOT NULL,
  is_email_valid BOOLEAN NOT NULL DEFAULT FALSE,
  terms_agreed BOOLEAN NOT NULL DEFAULT FALSE,
  login_date TIMESTAMP NULL,
  PRIMARY KEY (id)
);


-- -----------------------------------------------------
-- Table layer
-- -----------------------------------------------------
DROP TABLE IF EXISTS layer CASCADE ;

CREATE TABLE IF NOT EXISTS layer (
  id SERIAL ,
  table_name TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  description TEXT NULL,
  source_author_name TEXT NULL,
  created_at TIMESTAMP NOT NULL,
  removed_at TIMESTAMP NULL,
  is_published BOOLEAN NULL DEFAULT FALSE,
  fk_user_id_author INT NOT NULL,
  fk_user_id_published_by INT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_project_user1
    FOREIGN KEY (fk_user_id_author)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_layer_user_1
    FOREIGN KEY (fk_user_id_published_by)
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
  description TEXT NULL,
  created_at TIMESTAMP NOT NULL,
  closed_at TIMESTAMP NULL,
  fk_user_id INT NOT NULL,
  fk_layer_id INT NOT NULL,
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
-- Table version_feature
-- -----------------------------------------------------
DROP TABLE IF EXISTS version_feature CASCADE ;

CREATE TABLE IF NOT EXISTS version_feature (
  id SERIAL ,
  geom GEOMETRY(GEOMETRYCOLLECTION, 4326) NOT NULL,
  start_date TIMESTAMP NULL,
  end_date TIMESTAMP NULL,
  file TEXT NULL,
  version INT NOT NULL DEFAULT 1,
  visible BOOLEAN NOT NULL DEFAULT TRUE,
  fk_changeset_id INT NOT NULL,
  PRIMARY KEY (id, version),
  CONSTRAINT fk_tb_contribution_tb_project1
    FOREIGN KEY (fk_changeset_id)
    REFERENCES changeset (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table auth
-- -----------------------------------------------------
DROP TABLE IF EXISTS auth CASCADE ;

CREATE TABLE IF NOT EXISTS auth (
  id SERIAL ,
  is_admin BOOLEAN NOT NULL DEFAULT FALSE,
  is_manager BOOLEAN NOT NULL,
  is_curator BOOLEAN NOT NULL,
  fk_user_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_auth_user1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table user_layer
-- -----------------------------------------------------
DROP TABLE IF EXISTS user_layer CASCADE ;

CREATE TABLE IF NOT EXISTS user_layer (
  fk_user_id INT NOT NULL,
  fk_layer_id INT NOT NULL,
  created_at TIMESTAMP NULL,
  PRIMARY KEY (fk_user_id, fk_layer_id),
  CONSTRAINT fk_project_subscriber_user1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_user_layer_layer1
    FOREIGN KEY (fk_layer_id)
    REFERENCES layer (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table feature
-- -----------------------------------------------------
DROP TABLE IF EXISTS feature CASCADE ;

CREATE TABLE IF NOT EXISTS feature (
  id SERIAL ,
  geom GEOMETRY(GEOMETRYCOLLECTION, 4326) NOT NULL,
  start_date TIMESTAMP NULL,
  end_date TIMESTAMP NULL,
  file TEXT NULL,
  version INT NOT NULL DEFAULT 1,
  fk_changeset_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_tb_contribution_tb_project10
    FOREIGN KEY (fk_changeset_id)
    REFERENCES changeset (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table review
-- -----------------------------------------------------
DROP TABLE IF EXISTS review CASCADE ;

CREATE TABLE IF NOT EXISTS review (
  id SERIAL ,
  description TEXT NOT NULL,
  create_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NULL,
  closed_at TIMESTAMP NULL,
  fk_user_id INT NOT NULL,
  fk_layer_id INT NOT NULL,
  fk_parent_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_review_layer1
    FOREIGN KEY (fk_layer_id)
    REFERENCES layer (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_review_user_1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_layer_comment_layer_comment1
    FOREIGN KEY (fk_parent_id)
    REFERENCES review (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table theme
-- -----------------------------------------------------
DROP TABLE IF EXISTS theme CASCADE ;

CREATE TABLE IF NOT EXISTS theme (
  id SERIAL ,
  name TEXT NULL,
  created_at TIMESTAMP NULL,
  fk_parent_id INT NULL,
  fk_user_id_creator INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_theme_theme1
    FOREIGN KEY (fk_parent_id)
    REFERENCES theme (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_theme_user_1
    FOREIGN KEY (fk_user_id_creator)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table notification
-- -----------------------------------------------------
DROP TABLE IF EXISTS notification CASCADE ;

CREATE TABLE IF NOT EXISTS notification (
  id SERIAL ,
  name TEXT NOT NULL,
  description TEXT NOT NULL,
  icon TEXT NULL,
  created_at TIMESTAMP NOT NULL,
  fk_user_id INT NULL,
  fk_layer_id INT NULL,
  fk_theme_id INT NULL,
  fk_review_id INT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_notification_layer1
    FOREIGN KEY (fk_layer_id)
    REFERENCES layer (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_notification_layer_review1
    FOREIGN KEY (fk_review_id)
    REFERENCES review (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_notification_theme1
    FOREIGN KEY (fk_theme_id)
    REFERENCES theme (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_notification_user_1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table user_notification
-- -----------------------------------------------------
DROP TABLE IF EXISTS user_notification CASCADE ;

CREATE TABLE IF NOT EXISTS user_notification (
  fk_user_id INT NOT NULL,
  fk_notification_id INT NOT NULL,
  is_read BOOLEAN NULL DEFAULT FALSE,
  CONSTRAINT fk_user_notification_user_1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_user_notification_notification1
    FOREIGN KEY (fk_notification_id)
    REFERENCES notification (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table bulk_import
-- -----------------------------------------------------
DROP TABLE IF EXISTS bulk_import CASCADE ;

CREATE TABLE IF NOT EXISTS bulk_import (
  id SERIAL ,
  file BYTEA NULL,
  description TEXT NULL,
  accepted BOOLEAN NULL,
  created_at VARCHAR(45) NULL,
  accepted_at VARCHAR(45) NULL,
  fk_user_id INT NOT NULL,
  fk_layer_id INT NOT NULL,
  fk_user_id_curator INT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_bulk_import_user_1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_bulk_import_layer1
    FOREIGN KEY (fk_layer_id)
    REFERENCES layer (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_bulk_import_user_2
    FOREIGN KEY (fk_user_id_curator)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table layer_followers
-- -----------------------------------------------------
DROP TABLE IF EXISTS layer_followers CASCADE ;

CREATE TABLE IF NOT EXISTS layer_followers (
  fk_user_id INT NOT NULL,
  fk_layer_id INT NOT NULL,
  created_at TIMESTAMP NULL,
  PRIMARY KEY (fk_user_id, fk_layer_id),
  CONSTRAINT fk_user_follows_layer_user_1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_user_follows_layer_layer1
    FOREIGN KEY (fk_layer_id)
    REFERENCES layer (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table theme_followers
-- -----------------------------------------------------
DROP TABLE IF EXISTS theme_followers CASCADE ;

CREATE TABLE IF NOT EXISTS theme_followers (
  fk_user_id INT NOT NULL,
  fk_theme_id INT NOT NULL,
  created_at TIMESTAMP NULL,
  PRIMARY KEY (fk_theme_id, fk_user_id),
  CONSTRAINT fk_user_follows_theme_user_1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_user_follows_theme_theme1
    FOREIGN KEY (fk_theme_id)
    REFERENCES theme (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table reference_
-- -----------------------------------------------------
DROP TABLE IF EXISTS reference_ CASCADE ;

CREATE TABLE IF NOT EXISTS reference_ (
  id SERIAL ,
  description TEXT NULL,
  fk_layer_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_reference_layer1
    FOREIGN KEY (fk_layer_id)
    REFERENCES layer (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table curator
-- -----------------------------------------------------
DROP TABLE IF EXISTS curator CASCADE ;

CREATE TABLE IF NOT EXISTS curator (
  fk_user_id INT NOT NULL,
  fk_theme_id INT NOT NULL,
  region TEXT NULL,
  fk_user_id_creator INT NOT NULL,
  CONSTRAINT fk_curator_user_theme_user_1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_curator_user_theme_theme1
    FOREIGN KEY (fk_theme_id)
    REFERENCES theme (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_curator_user_1
    FOREIGN KEY (fk_user_id_creator)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table layer_theme
-- -----------------------------------------------------
DROP TABLE IF EXISTS layer_theme CASCADE ;

CREATE TABLE IF NOT EXISTS layer_theme (
  fk_layer_id INT NOT NULL,
  fk_theme_id INT NOT NULL,
  CONSTRAINT fk_layer_theme_layer1
    FOREIGN KEY (fk_layer_id)
    REFERENCES layer (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_layer_theme_theme1
    FOREIGN KEY (fk_theme_id)
    REFERENCES theme (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table comment
-- -----------------------------------------------------
DROP TABLE IF EXISTS comment CASCADE ;

CREATE TABLE IF NOT EXISTS comment (
  id SERIAL ,
  body TEXT NULL,
  created_at TIMESTAMP NULL,
  fk_layer_id INT NOT NULL,
  fk_user_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_comment_layer1
    FOREIGN KEY (fk_layer_id)
    REFERENCES layer (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_comment_user_1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);
