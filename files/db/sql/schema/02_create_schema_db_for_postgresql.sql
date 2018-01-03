
-- Ter 02 Jan 2018 16:13:29 -02

-- -----------------------------------------------------
-- Table user_
-- -----------------------------------------------------
DROP TABLE IF EXISTS user_ CASCADE ;

CREATE TABLE IF NOT EXISTS user_ (
  id SERIAL ,
  username VARCHAR(45) NOT NULL,
  email VARCHAR(45) NOT NULL,
  password VARCHAR(45) NOT NULL,
  is_email_valid BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL,
  removed_at TIMESTAMP NULL,
  terms_agreed BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (id)
);


-- -----------------------------------------------------
-- Table group_
-- -----------------------------------------------------
DROP TABLE IF EXISTS group_ CASCADE ;

CREATE TABLE IF NOT EXISTS group_ (
  id SERIAL ,
  created_at TIMESTAMP NOT NULL,
  removed_at TIMESTAMP NULL,
  visible BOOLEAN NOT NULL DEFAULT TRUE,
  fk_user_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_group__user_1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table project
-- -----------------------------------------------------
DROP TABLE IF EXISTS project CASCADE ;

CREATE TABLE IF NOT EXISTS project (
  id SERIAL ,
  created_at TIMESTAMP NOT NULL,
  removed_at TIMESTAMP NULL,
  visible BOOLEAN NOT NULL DEFAULT TRUE,
  fk_group_id INT NOT NULL,
  fk_user_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_project_user_1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_project_group1
    FOREIGN KEY (fk_group_id)
    REFERENCES group_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table layer
-- -----------------------------------------------------
DROP TABLE IF EXISTS layer CASCADE ;

CREATE TABLE IF NOT EXISTS layer (
  id SERIAL ,
  created_at TIMESTAMP NOT NULL,
  removed_at TIMESTAMP NULL,
  visible BOOLEAN NOT NULL DEFAULT TRUE,
  fk_project_id INT NOT NULL,
  fk_user_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_project_user1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_layer_project1
    FOREIGN KEY (fk_project_id)
    REFERENCES project (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table changeset
-- -----------------------------------------------------
DROP TABLE IF EXISTS changeset CASCADE ;

CREATE TABLE IF NOT EXISTS changeset (
  id SERIAL ,
  created_at TIMESTAMP NOT NULL,
  closed_at TIMESTAMP NULL,
  visible BOOLEAN NOT NULL DEFAULT TRUE,
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
  geom GEOMETRY(MULTIPOINT, 4326) NOT NULL,
  visible BOOLEAN NOT NULL DEFAULT TRUE,
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
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NOT NULL,
  fk_user_id INT NOT NULL,
  PRIMARY KEY (k, fk_user_id),
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
  body TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NULL,
  removed_at TIMESTAMP NULL,
  visible BOOLEAN NOT NULL DEFAULT TRUE,
  fk_changeset_id INT NOT NULL,
  fk_user_id INT NOT NULL,
  fk_comment_id_parent INT NOT NULL,
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
    ON UPDATE CASCADE,
  CONSTRAINT fk_changeset_comment_changeset_comment1
    FOREIGN KEY (fk_comment_id_parent)
    REFERENCES changeset_comment (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table line
-- -----------------------------------------------------
DROP TABLE IF EXISTS line CASCADE ;

CREATE TABLE IF NOT EXISTS line (
  id SERIAL ,
  geom GEOMETRY(MULTILINESTRING, 4326) NOT NULL,
  visible BOOLEAN NOT NULL DEFAULT TRUE,
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

CREATE TABLE IF NOT EXISTS line_tag (
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NOT NULL,
  fk_line_version INT NOT NULL,
  fk_line_id INT NOT NULL,
  PRIMARY KEY (k, fk_line_version, fk_line_id),
  CONSTRAINT fk_line_tag_line1
    FOREIGN KEY (fk_line_id , fk_line_version)
    REFERENCES line (id , version)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table point_tag
-- -----------------------------------------------------
DROP TABLE IF EXISTS point_tag CASCADE ;

CREATE TABLE IF NOT EXISTS point_tag (
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NOT NULL,
  fk_point_version INT NOT NULL,
  fk_point_id INT NOT NULL,
  PRIMARY KEY (k, fk_point_version, fk_point_id),
  CONSTRAINT fk_point_tag_point1
    FOREIGN KEY (fk_point_id , fk_point_version)
    REFERENCES point (id , version)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table user_comment
-- -----------------------------------------------------
DROP TABLE IF EXISTS user_comment CASCADE ;

CREATE TABLE IF NOT EXISTS user_comment (
  id SERIAL ,
  body TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NULL,
  removed_at TIMESTAMP NULL,
  is_read BOOLEAN NOT NULL DEFAULT FALSE,
  visible BOOLEAN NOT NULL DEFAULT TRUE,
  fk_user_id_from INT NOT NULL,
  fk_user_id_to INT NOT NULL,
  fk_comment_id_parent INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_message_user1
    FOREIGN KEY (fk_user_id_from)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_user_message_user_1
    FOREIGN KEY (fk_user_id_to)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_user_message_user_message1
    FOREIGN KEY (fk_comment_id_parent)
    REFERENCES user_comment (id)
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
  allow_bulk_import BOOLEAN NOT NULL DEFAULT FALSE,
  fk_user_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_auth_user1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table follow
-- -----------------------------------------------------
DROP TABLE IF EXISTS follow CASCADE ;

CREATE TABLE IF NOT EXISTS follow (
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
  geom GEOMETRY(MULTIPOLYGON, 4326) NOT NULL,
  visible BOOLEAN NOT NULL DEFAULT TRUE,
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

CREATE TABLE IF NOT EXISTS polygon_tag (
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NOT NULL,
  fk_polygon_version INT NOT NULL,
  fk_polygon_id INT NOT NULL,
  PRIMARY KEY (k, fk_polygon_version, fk_polygon_id),
  CONSTRAINT fk_polygon_tag_polygon1
    FOREIGN KEY (fk_polygon_id , fk_polygon_version)
    REFERENCES polygon (id , version)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table project_watcher
-- -----------------------------------------------------
DROP TABLE IF EXISTS project_watcher CASCADE ;

CREATE TABLE IF NOT EXISTS project_watcher (
  fk_project_id INT NOT NULL,
  fk_user_id INT NOT NULL,
  PRIMARY KEY (fk_project_id, fk_user_id),
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
  geom GEOMETRY(MULTIPOINT, 4326) NOT NULL,
  visible BOOLEAN NOT NULL DEFAULT TRUE,
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
-- Table current_polygon
-- -----------------------------------------------------
DROP TABLE IF EXISTS current_polygon CASCADE ;

CREATE TABLE IF NOT EXISTS current_polygon (
  id SERIAL ,
  geom GEOMETRY(MULTIPOLYGON, 4326) NOT NULL,
  visible BOOLEAN NOT NULL DEFAULT TRUE,
  version INT NOT NULL DEFAULT 1,
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

CREATE TABLE IF NOT EXISTS current_polygon_tag (
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NOT NULL,
  fk_current_polygon_id INT NOT NULL,
  PRIMARY KEY (k, fk_current_polygon_id),
  CONSTRAINT fk_current_area_tag_current_area1
    FOREIGN KEY (fk_current_polygon_id)
    REFERENCES current_polygon (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table current_line
-- -----------------------------------------------------
DROP TABLE IF EXISTS current_line CASCADE ;

CREATE TABLE IF NOT EXISTS current_line (
  id SERIAL ,
  geom GEOMETRY(MULTILINESTRING, 4326) NOT NULL,
  visible BOOLEAN NOT NULL DEFAULT TRUE,
  version INT NOT NULL DEFAULT 1,
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

CREATE TABLE IF NOT EXISTS current_line_tag (
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NOT NULL,
  fk_current_line_id INT NOT NULL,
  PRIMARY KEY (k, fk_current_line_id),
  CONSTRAINT fk_current_way_tag_current_way1
    FOREIGN KEY (fk_current_line_id)
    REFERENCES current_line (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table current_point_tag
-- -----------------------------------------------------
DROP TABLE IF EXISTS current_point_tag CASCADE ;

CREATE TABLE IF NOT EXISTS current_point_tag (
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NOT NULL,
  fk_current_point_id INT NOT NULL,
  PRIMARY KEY (k, fk_current_point_id),
  CONSTRAINT fk_current_node_tag_current_node1
    FOREIGN KEY (fk_current_point_id)
    REFERENCES current_point (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table changeset_tag
-- -----------------------------------------------------
DROP TABLE IF EXISTS changeset_tag CASCADE ;

CREATE TABLE IF NOT EXISTS changeset_tag (
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NOT NULL,
  fk_changeset_id INT NOT NULL,
  PRIMARY KEY (k, fk_changeset_id),
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
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NOT NULL,
  fk_layer_id INT NOT NULL,
  PRIMARY KEY (k, fk_layer_id),
  CONSTRAINT fk_project_tag_project1
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
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NOT NULL,
  fk_project_id INT NOT NULL,
  PRIMARY KEY (k, fk_project_id),
  CONSTRAINT fk_project_project1
    FOREIGN KEY (fk_project_id)
    REFERENCES project (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table layer_comment
-- -----------------------------------------------------
DROP TABLE IF EXISTS layer_comment CASCADE ;

CREATE TABLE IF NOT EXISTS layer_comment (
  id SERIAL ,
  body TEXT NOT NULL,
  create_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NULL,
  closed_at TIMESTAMP NULL,
  visible BOOLEAN NOT NULL DEFAULT TRUE,
  fk_layer_id INT NOT NULL,
  fk_user_id INT NOT NULL,
  fk_comment_id_parent INT NOT NULL,
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
    FOREIGN KEY (fk_comment_id_parent)
    REFERENCES layer_comment (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table layer_comment_award
-- -----------------------------------------------------
DROP TABLE IF EXISTS layer_comment_award CASCADE ;

CREATE TABLE IF NOT EXISTS layer_comment_award (
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NOT NULL,
  fk_comment_id INT NOT NULL,
  fk_user_id INT NOT NULL,
  PRIMARY KEY (k, fk_comment_id),
  CONSTRAINT fk_layer_comment_tag_layer_comment1
    FOREIGN KEY (fk_comment_id)
    REFERENCES layer_comment (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_layer_comment_award_user_1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table user_group
-- -----------------------------------------------------
DROP TABLE IF EXISTS user_group CASCADE ;

CREATE TABLE IF NOT EXISTS user_group (
  fk_group_id INT NOT NULL,
  fk_user_id INT NOT NULL,
  added_at TIMESTAMP NOT NULL,
  group_permission VARCHAR(10) NOT NULL DEFAULT 'member',
  can_receive_notification BOOLEAN NOT NULL DEFAULT TRUE,
  fk_user_id_added_by INT NOT NULL,
  PRIMARY KEY (fk_group_id, fk_user_id),
  CONSTRAINT fk_user_group_user_1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_user_group_group1
    FOREIGN KEY (fk_group_id)
    REFERENCES group_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_user_group_user_2
    FOREIGN KEY (fk_user_id_added_by)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table polygon_award
-- -----------------------------------------------------
DROP TABLE IF EXISTS polygon_award CASCADE ;

CREATE TABLE IF NOT EXISTS polygon_award (
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NOT NULL,
  fk_polygon_version INT NOT NULL,
  fk_polygon_id INT NOT NULL,
  fk_user_id INT NOT NULL,
  PRIMARY KEY (k, fk_polygon_version, fk_polygon_id),
  CONSTRAINT fk_polygon_award_polygon1
    FOREIGN KEY (fk_polygon_id , fk_polygon_version)
    REFERENCES polygon (id , version)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_polygon_award_user_1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table point_award
-- -----------------------------------------------------
DROP TABLE IF EXISTS point_award CASCADE ;

CREATE TABLE IF NOT EXISTS point_award (
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NOT NULL,
  fk_point_version INT NOT NULL,
  fk_point_id INT NOT NULL,
  fk_user_id INT NOT NULL,
  PRIMARY KEY (k, fk_point_version, fk_point_id),
  CONSTRAINT fk_point_award_point1
    FOREIGN KEY (fk_point_id , fk_point_version)
    REFERENCES point (id , version)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_point_award_user_1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table line_award
-- -----------------------------------------------------
DROP TABLE IF EXISTS line_award CASCADE ;

CREATE TABLE IF NOT EXISTS line_award (
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NOT NULL,
  fk_line_version INT NOT NULL,
  fk_line_id INT NOT NULL,
  fk_user_id INT NOT NULL,
  PRIMARY KEY (k, fk_line_version, fk_line_id),
  CONSTRAINT fk_line_award_line1
    FOREIGN KEY (fk_line_id , fk_line_version)
    REFERENCES line (id , version)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_line_award_user_1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table current_point_award
-- -----------------------------------------------------
DROP TABLE IF EXISTS current_point_award CASCADE ;

CREATE TABLE IF NOT EXISTS current_point_award (
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NOT NULL,
  fk_current_point_id INT NOT NULL,
  fk_user_id INT NOT NULL,
  PRIMARY KEY (k, fk_current_point_id),
  CONSTRAINT fk_current_point_award_current_point1
    FOREIGN KEY (fk_current_point_id)
    REFERENCES current_point (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_current_point_award_user_1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table current_line_award
-- -----------------------------------------------------
DROP TABLE IF EXISTS current_line_award CASCADE ;

CREATE TABLE IF NOT EXISTS current_line_award (
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NOT NULL,
  fk_current_line_id INT NOT NULL,
  fk_user_id INT NOT NULL,
  PRIMARY KEY (k, fk_current_line_id),
  CONSTRAINT fk_current_line_award_current_line1
    FOREIGN KEY (fk_current_line_id)
    REFERENCES current_line (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_current_line_award_user_1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table current_polygon_award
-- -----------------------------------------------------
DROP TABLE IF EXISTS current_polygon_award CASCADE ;

CREATE TABLE IF NOT EXISTS current_polygon_award (
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NOT NULL,
  fk_current_polygon_id INT NOT NULL,
  fk_user_id INT NOT NULL,
  PRIMARY KEY (k, fk_current_polygon_id),
  CONSTRAINT fk_current_polygon_award_current_polygon1
    FOREIGN KEY (fk_current_polygon_id)
    REFERENCES current_polygon (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_current_polygon_award_user_1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table user_award
-- -----------------------------------------------------
DROP TABLE IF EXISTS user_award CASCADE ;

CREATE TABLE IF NOT EXISTS user_award (
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NOT NULL,
  fk_user_id INT NOT NULL,
  PRIMARY KEY (k, fk_user_id),
  CONSTRAINT fk_user_award_user_1
    FOREIGN KEY (fk_user_id)
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
  created_at TIMESTAMP NOT NULL,
  removed_at TIMESTAMP NULL,
  is_read BOOLEAN NOT NULL DEFAULT FALSE,
  visible BOOLEAN NOT NULL DEFAULT TRUE,
  fk_user_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_notification_user_1
    FOREIGN KEY (fk_user_id)
    REFERENCES user_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table group_tag
-- -----------------------------------------------------
DROP TABLE IF EXISTS group_tag CASCADE ;

CREATE TABLE IF NOT EXISTS group_tag (
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NOT NULL,
  fk_group_id INT NOT NULL,
  PRIMARY KEY (k, fk_group_id),
  CONSTRAINT fk_group_tag_group_1
    FOREIGN KEY (fk_group_id)
    REFERENCES group_ (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table notification_tag
-- -----------------------------------------------------
DROP TABLE IF EXISTS notification_tag CASCADE ;

CREATE TABLE IF NOT EXISTS notification_tag (
  k VARCHAR(255) NOT NULL,
  v VARCHAR(255) NOT NULL,
  fk_notification_id INT NOT NULL,
  PRIMARY KEY (k, fk_notification_id),
  CONSTRAINT fk_notification_tag_notification1
    FOREIGN KEY (fk_notification_id)
    REFERENCES notification (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);
