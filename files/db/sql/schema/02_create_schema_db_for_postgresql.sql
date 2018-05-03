
-- Qua 02 Mai 2018 16:11:26 -03

-- -----------------------------------------------------
-- Table pauliceia_user
-- -----------------------------------------------------
DROP TABLE IF EXISTS pauliceia_user CASCADE ;

CREATE TABLE IF NOT EXISTS pauliceia_user (
  user_id SERIAL ,
  email TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL,
  username TEXT NOT NULL UNIQUE,
  name TEXT NULL,
  created_at TIMESTAMP NOT NULL,
  is_email_valid BOOLEAN NOT NULL DEFAULT FALSE,
  terms_agreed BOOLEAN NOT NULL DEFAULT FALSE,
  login_date TIMESTAMP NULL,
  is_the_admin BOOLEAN NOT NULL  DEFAULT FALSE,
  can_add_layer BOOLEAN NOT NULL DEFAULT FALSE,
  receive_notification_by_email BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (user_id)
);


-- -----------------------------------------------------
-- Table layer
-- -----------------------------------------------------
DROP TABLE IF EXISTS layer CASCADE ;

CREATE TABLE IF NOT EXISTS layer (
  layer_id SERIAL ,
  f_table_name TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  description TEXT NULL,
  source_description TEXT NULL ,
  created_at TIMESTAMP NOT NULL,
  is_published BOOLEAN NOT NULL DEFAULT FALSE,
  user_id_published_by INT NULL,
  PRIMARY KEY (layer_id),
  CONSTRAINT fk_layer_user_1
    FOREIGN KEY (user_id_published_by)
    REFERENCES pauliceia_user (user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table changeset
-- -----------------------------------------------------
DROP TABLE IF EXISTS changeset CASCADE ;

CREATE TABLE IF NOT EXISTS changeset (
  changeset_id SERIAL ,
  description TEXT NULL,
  created_at TIMESTAMP NOT NULL,
  closed_at TIMESTAMP NULL,
  user_id INT NOT NULL,
  layer_id INT NOT NULL,
  PRIMARY KEY (changeset_id),
  CONSTRAINT fk_tb_project_tb_user1
    FOREIGN KEY (user_id)
    REFERENCES pauliceia_user (user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_change_set_project1
    FOREIGN KEY (layer_id)
    REFERENCES layer (layer_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------

-- -----------------------------------------------------
-- Table user_layer
-- -----------------------------------------------------
DROP TABLE IF EXISTS user_layer CASCADE ;

CREATE TABLE IF NOT EXISTS user_layer (
  user_id SERIAL ,
  layer_id INT NOT NULL,
  created_at TIMESTAMP NULL,
  is_the_creator BOOLEAN NULL ,
  PRIMARY KEY (user_id, layer_id),
  CONSTRAINT fk_project_subscriber_user1
    FOREIGN KEY (user_id)
    REFERENCES pauliceia_user (user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_user_layer_layer1
    FOREIGN KEY (layer_id)
    REFERENCES layer (layer_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- -----------------------------------------------------
-- Table theme
-- -----------------------------------------------------
DROP TABLE IF EXISTS theme CASCADE ;

CREATE TABLE IF NOT EXISTS theme (
  theme_id SERIAL ,
  name TEXT NULL,
  created_at TIMESTAMP NULL,
  parent_id INT NULL,
  user_id_creator INT NOT NULL,
  PRIMARY KEY (theme_id),
  CONSTRAINT fk_theme_theme1
    FOREIGN KEY (parent_id)
    REFERENCES theme (theme_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_theme_user1
    FOREIGN KEY (user_id_creator)
    REFERENCES pauliceia_user (user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table notification
-- -----------------------------------------------------
DROP TABLE IF EXISTS notification CASCADE ;

CREATE TABLE IF NOT EXISTS notification (
  notification_id SERIAL ,
  name TEXT NOT NULL,
  description TEXT NOT NULL ,
  icon TEXT NULL,
  created_at TIMESTAMP NOT NULL,
  user_id INT NULL ,
  layer_id INT NULL ,
  theme_id INT NULL ,
  notification_id_parent INT NULL,
  PRIMARY KEY (notification_id),
  CONSTRAINT fk_notification_layer1
    FOREIGN KEY (layer_id)
    REFERENCES layer (layer_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_notification_theme1
    FOREIGN KEY (theme_id)
    REFERENCES theme (theme_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_notification_user_1
    FOREIGN KEY (user_id)
    REFERENCES pauliceia_user (user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_notification_notification1
    FOREIGN KEY (notification_id_parent)
    REFERENCES notification (notification_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table user_notification
-- -----------------------------------------------------
DROP TABLE IF EXISTS user_notification CASCADE ;

CREATE TABLE IF NOT EXISTS user_notification (
  user_id SERIAL ,
  notification_id INT NOT NULL,
  is_read BOOLEAN NULL DEFAULT FALSE,
  CONSTRAINT fk_user_notification_user_1
    FOREIGN KEY (user_id)
    REFERENCES pauliceia_user (user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_user_notification_notification1
    FOREIGN KEY (notification_id)
    REFERENCES notification (notification_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table layer_followers
-- -----------------------------------------------------
DROP TABLE IF EXISTS layer_followers CASCADE ;

CREATE TABLE IF NOT EXISTS layer_followers (
  user_id SERIAL ,
  layer_id INT NOT NULL,
  created_at TIMESTAMP NULL,
  PRIMARY KEY (user_id, layer_id),
  CONSTRAINT fk_user_follows_layer_user_1
    FOREIGN KEY (user_id)
    REFERENCES pauliceia_user (user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_user_follows_layer_layer1
    FOREIGN KEY (layer_id)
    REFERENCES layer (layer_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table theme_followers
-- -----------------------------------------------------
DROP TABLE IF EXISTS theme_followers CASCADE ;

CREATE TABLE IF NOT EXISTS theme_followers (
  user_id SERIAL ,
  theme_id INT NOT NULL,
  created_at TIMESTAMP NULL,
  PRIMARY KEY (theme_id, user_id),
  CONSTRAINT fk_user_follows_theme_user_1
    FOREIGN KEY (user_id)
    REFERENCES pauliceia_user (user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_user_follows_theme_theme1
    FOREIGN KEY (theme_id)
    REFERENCES theme (theme_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table reference_
-- -----------------------------------------------------
DROP TABLE IF EXISTS reference_ CASCADE ;

CREATE TABLE IF NOT EXISTS reference_ (
  reference_id SERIAL ,
  bibtex TEXT NULL ,
  PRIMARY KEY (reference_id)
);


-- -----------------------------------------------------
-- Table curator
-- -----------------------------------------------------
DROP TABLE IF EXISTS curator CASCADE ;

CREATE TABLE IF NOT EXISTS curator (
  user_id SERIAL  ,
  theme_id INT NOT NULL,
  region TEXT NULL,
  created_at TIMESTAMP NULL,
  CONSTRAINT fk_curator_user_theme_user_1
    FOREIGN KEY (user_id)
    REFERENCES pauliceia_user (user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_curator_user_theme_theme1
    FOREIGN KEY (theme_id)
    REFERENCES theme (theme_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table layer_theme
-- -----------------------------------------------------
DROP TABLE IF EXISTS layer_theme CASCADE ;

CREATE TABLE IF NOT EXISTS layer_theme (
  layer_id SERIAL ,
  theme_id INT NOT NULL,
  CONSTRAINT fk_layer_theme_layer1
    FOREIGN KEY (layer_id)
    REFERENCES layer (layer_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_layer_theme_theme1
    FOREIGN KEY (theme_id)
    REFERENCES theme (theme_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table reference_layer
-- -----------------------------------------------------
DROP TABLE IF EXISTS reference_layer CASCADE ;

CREATE TABLE IF NOT EXISTS reference_layer (
  layer_id SERIAL ,
  reference_id INT NOT NULL,
  PRIMARY KEY (layer_id, reference_id),
  CONSTRAINT fk_reference_layer_layer1
    FOREIGN KEY (layer_id)
    REFERENCES layer (layer_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_reference_layer_reference1
    FOREIGN KEY (reference_id)
    REFERENCES reference_ (reference_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table reference
-- -----------------------------------------------------
DROP TABLE IF EXISTS reference CASCADE ;

CREATE TABLE IF NOT EXISTS reference (
  reference_id SERIAL ,
  bibtex TEXT NULL,
  layer_id INT NOT NULL,
  PRIMARY KEY (reference_id),
  CONSTRAINT fk_reference_layer1
    FOREIGN KEY (layer_id)
    REFERENCES layer (layer_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);
