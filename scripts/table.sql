CREATE database if not exists asset_app;
USE asset_app;
CREATE TABLE if not exists `asset` (
                                       `name` VARCHAR(255),
                                       `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                                       `owner` VARCHAR(255),
                                       `description` VARCHAR(1000),
                                       `location` VARCHAR(1000),
                                       `criticality` enum('Critical','Medium','Low') DEFAULT 'Low',
                                        FULLTEXT ftidx (`name`)
) ENGINE=InnoDB;


CREATE TABLE if not exists `user` (
                                      `username` VARCHAR(255),
                                      `name` varchar(255),
                                      `password` VARCHAR(1024),
                                      `salt` VARCHAR(1024),
                                      `admin` boolean DEFAULT false,
                                      UNIQUE KEY `idexun` (`username`) USING BTREE,
                                      PRIMARY KEY (`username`)
) ENGINE=InnoDB;

INSERT INTO asset_app.user (username, name, password, salt, admin)
VALUES ('bob', 'Bob Anderson', 'password', 'mysalt', 1);
