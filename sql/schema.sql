
-- creating the database

DROP DATABASE IF EXISTS melbournePlace;
CREATE DATABASE melbournePlace;
USE melbournePlace;

-- user table

CREATE TABLE users (

    id INT NOT NULL AUTO_INCREMENT,
    nickname VARCHAR(256),

    PRIMARY KEY (id)

);

-- rings table

CREATE TABLE ringRequests (

    id INT NOT NULL,
    ip VARCHAR(128),
    time TIMESTAMP NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES users(id)

);

-- create a user

CREATE USER "melbournePlace"@"localhost" IDENTIFIED BY "J1#23h7c$?.##{<#";
GRANT ALL PRIVILEGES ON melbournePlace . * TO "melbournePlace"@"localhost";
