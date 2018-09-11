
-- delete all tables in public schema, with exception of the spatial_ref_sys
-- SOURCE: https://stackoverflow.com/questions/3327312/drop-all-tables-in-postgresql
DO $$ DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public' and tablename != 'spatial_ref_sys') LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END $$;


-- Ter 11 Set 2018 15:55:39 -03

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
  is_the_admin BOOLEAN NOT NULL DEFAULT FALSE ,
  receive_notification_by_email BOOLEAN NOT NULL,
  picture TEXT NULL,
  social_id TEXT NULL,
  social_account TEXT NULL,
  language TEXT NULL,
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
  PRIMARY KEY (layer_id)
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
  user_id_creator INT NOT NULL,
  layer_id INT NOT NULL,
  PRIMARY KEY (changeset_id),
  CONSTRAINT fk_tb_project_tb_user1
    FOREIGN KEY (user_id_creator)
    REFERENCES pauliceia_user (user_id)
    ON DELETE NO ACTION
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
  is_the_creator BOOLEAN NULL DEFAULT FALSE ,
  PRIMARY KEY (user_id, layer_id),
  CONSTRAINT fk_project_subscriber_user1
    FOREIGN KEY (user_id)
    REFERENCES pauliceia_user (user_id)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  CONSTRAINT fk_user_layer_layer1
    FOREIGN KEY (layer_id)
    REFERENCES layer (layer_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------

-- -----------------------------------------------------
-- Table keyword
-- -----------------------------------------------------
DROP TABLE IF EXISTS keyword CASCADE ;

CREATE TABLE IF NOT EXISTS keyword (
  keyword_id SERIAL ,
  name TEXT NOT NULL UNIQUE,
  created_at TIMESTAMP NULL,
  user_id_creator INT NOT NULL,
  PRIMARY KEY (keyword_id),
  CONSTRAINT fk_theme_user1
    FOREIGN KEY (user_id_creator)
    REFERENCES pauliceia_user (user_id)
    ON DELETE NO ACTION
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table notification
-- -----------------------------------------------------
DROP TABLE IF EXISTS notification CASCADE ;

CREATE TABLE IF NOT EXISTS notification (
  notification_id SERIAL ,
  description TEXT NOT NULL ,
  created_at TIMESTAMP NOT NULL,
  is_denunciation BOOLEAN NOT NULL DEFAULT FALSE,
  user_id_creator INT NOT NULL ,
  layer_id INT NULL ,
  keyword_id INT NULL ,
  notification_id_parent INT NULL,
  PRIMARY KEY (notification_id),
  CONSTRAINT fk_notification_layer1
    FOREIGN KEY (layer_id)
    REFERENCES layer (layer_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_notification_theme1
    FOREIGN KEY (keyword_id)
    REFERENCES keyword (keyword_id)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  CONSTRAINT fk_notification_user_1
    FOREIGN KEY (user_id_creator)
    REFERENCES pauliceia_user (user_id)
    ON DELETE NO ACTION
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
  is_read BOOLEAN NULL,
  PRIMARY KEY (user_id, notification_id),
  CONSTRAINT fk_user_notification_user_1
    FOREIGN KEY (user_id)
    REFERENCES pauliceia_user (user_id)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  CONSTRAINT fk_user_notification_notification1
    FOREIGN KEY (notification_id)
    REFERENCES notification (notification_id)
    ON DELETE NO ACTION
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
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  CONSTRAINT fk_user_follows_layer_layer1
    FOREIGN KEY (layer_id)
    REFERENCES layer (layer_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table keyword_followers
-- -----------------------------------------------------
DROP TABLE IF EXISTS keyword_followers CASCADE ;

CREATE TABLE IF NOT EXISTS keyword_followers (
  user_id SERIAL ,
  keyword_id INT NOT NULL,
  created_at TIMESTAMP NULL,
  PRIMARY KEY (keyword_id, user_id),
  CONSTRAINT fk_user_follows_theme_user_1
    FOREIGN KEY (user_id)
    REFERENCES pauliceia_user (user_id)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  CONSTRAINT fk_user_follows_theme_theme1
    FOREIGN KEY (keyword_id)
    REFERENCES keyword (keyword_id)
    ON DELETE NO ACTION
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table reference
-- -----------------------------------------------------
DROP TABLE IF EXISTS reference CASCADE ;

CREATE TABLE IF NOT EXISTS reference (
  reference_id SERIAL ,
  description TEXT NOT NULL ,
  user_id_creator INT NOT NULL,
  PRIMARY KEY (reference_id),
  CONSTRAINT fk_reference_pauliceia_user1
    FOREIGN KEY (user_id_creator)
    REFERENCES pauliceia_user (user_id)
    ON DELETE NO ACTION
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table curator
-- -----------------------------------------------------
DROP TABLE IF EXISTS curator CASCADE ;

CREATE TABLE IF NOT EXISTS curator (
  user_id SERIAL  ,
  keyword_id INT NOT NULL,
  region TEXT NULL,
  created_at TIMESTAMP NULL,
  PRIMARY KEY (user_id, keyword_id),
  CONSTRAINT fk_curator_user_theme_user_1
    FOREIGN KEY (user_id)
    REFERENCES pauliceia_user (user_id)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  CONSTRAINT fk_curator_user_theme_theme1
    FOREIGN KEY (keyword_id)
    REFERENCES keyword (keyword_id)
    ON DELETE NO ACTION
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table layer_keyword
-- -----------------------------------------------------
DROP TABLE IF EXISTS layer_keyword CASCADE ;

CREATE TABLE IF NOT EXISTS layer_keyword (
  layer_id SERIAL ,
  keyword_id INT NOT NULL,
  PRIMARY KEY (layer_id, keyword_id),
  CONSTRAINT fk_layer_theme_layer1
    FOREIGN KEY (layer_id)
    REFERENCES layer (layer_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_layer_theme_theme1
    FOREIGN KEY (keyword_id)
    REFERENCES keyword (keyword_id)
    ON DELETE NO ACTION
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table layer_reference
-- -----------------------------------------------------
DROP TABLE IF EXISTS layer_reference CASCADE ;

CREATE TABLE IF NOT EXISTS layer_reference (
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
    REFERENCES reference (reference_id)
    ON DELETE NO ACTION
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table file
-- -----------------------------------------------------
DROP TABLE IF EXISTS file CASCADE ;

CREATE TABLE IF NOT EXISTS file (
  file_id SERIAL ,
  f_table_name TEXT NOT NULL UNIQUE,
  feature_id INT NOT NULL,
  name TEXT NULL,
  extension TEXT NULL,
  PRIMARY KEY (file_id, f_table_name, feature_id)
);


-- -----------------------------------------------------
-- Table mask
-- -----------------------------------------------------
DROP TABLE IF EXISTS mask CASCADE ;

CREATE TABLE IF NOT EXISTS mask (
  mask_id SERIAL ,
  mask TEXT NULL,
  PRIMARY KEY (mask_id)
);


-- -----------------------------------------------------
-- Table temporal_columns
-- -----------------------------------------------------
DROP TABLE IF EXISTS temporal_columns CASCADE ;

CREATE TABLE IF NOT EXISTS temporal_columns (
  f_table_name TEXT NOT NULL UNIQUE,
  start_date_column_name TEXT NULL,
  end_date_column_name TEXT NULL,
  start_date TIMESTAMP NOT NULL,
  end_date TIMESTAMP NOT NULL,
  start_date_mask_id INT NULL,
  end_date_mask_id INT NULL,
  PRIMARY KEY (f_table_name),
  CONSTRAINT fk_temporal_columns_mask1
    FOREIGN KEY (start_date_mask_id)
    REFERENCES mask (mask_id)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  CONSTRAINT fk_temporal_columns_mask2
    FOREIGN KEY (end_date_mask_id)
    REFERENCES mask (mask_id)
    ON DELETE NO ACTION
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table media_columns
-- -----------------------------------------------------
DROP TABLE IF EXISTS media_columns CASCADE ;

CREATE TABLE IF NOT EXISTS media_columns (
  f_table_name TEXT NOT NULL UNIQUE,
  media_column_name TEXT NOT NULL,
  media_type TEXT NULL,
  PRIMARY KEY (f_table_name, media_column_name)
);
