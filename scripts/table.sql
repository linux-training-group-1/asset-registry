-- Table structure for Asset Application
CREATE database if not exists asset_db;
USE asset_db;
create table asset
(
    asset_id    INT           NOT NULL AUTO_INCREMENT,
    name        VARCHAR(50)   NOT NULL unique,
    owner       VARCHAR(50)   NOT NULL,
    description VARCHAR(1024) NOT NULL,
    location    VARCHAR(50)   NOT NULL,
    criticality VARCHAR(10)   NOT NULL,
    PRIMARY KEY (asset_id)
);

create table user
(
    user_id  int          not null primary key auto_increment,
    username varchar(128) not null unique,
    pwd      varchar(128) not null
);
insert into asset_db.`user` (user_id, username, pwd) VALUES (1,'admin','$2a$12$9AXmYWNIHyPd/5HWytBVu.bq3oQ7yy5arXF2Pqf3Q7UGbQJrxzfrS');
-- user name is admin, password is password

-- database user creation
-- create user 'asset-app'@'%' identified by 'password';
-- mitigate the mysql bug https://stackoverflow.com/questions/5555328/error-1396-hy000-operation-create-user-failed-for-jacklocalhost
DROP user 'asset-app'@'%';
flush privileges ;
create user 'asset-app'@'%' identified by 'password';
grant all privileges on asset_db.* to 'asset-app'@'%';
