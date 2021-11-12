CREATE database if not exists asset_app;
USE asset_app;
CREATE TABLE if not exists `asset` (
                                       `name` VARCHAR(255),
                                       `id` INT NOT NULL,
                                       `owner` VARCHAR(255),
                                       `description` VARCHAR(1000),
                                       `location` VARCHAR(1000),
                                       `criticality` enum('Critical','Medium','Low') DEFAULT 'Low',
                                       UNIQUE KEY `idex` (`id`) USING BTREE,
                                       PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE TABLE if not exists `user` (
                                       `username` VARCHAR(255),
                                       `password` VARCHAR(255),
                                       `salt` VARCHAR(255),
                                       'admin' boolean default FALSE,
                                       UNIQUE KEY `idexun` (`username`) USING BTREE,
                                       PRIMARY KEY (`username`)
) ENGINE=InnoDB;