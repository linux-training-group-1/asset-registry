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