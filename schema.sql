CREATE DATABASE IF NOT EXISTS iot_b3
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE iot_b3;

CREATE TABLE telemetry (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    ts_utc DATETIME(3) NOT NULL,            
    device VARCHAR(32) NOT NULL,         
    topic VARCHAR(255) NOT NULL,     
    value DOUBLE NULL,          
    unit VARCHAR(16) NULL,         
    payload TEXT NOT NULL, 
    PRIMARY KEY (id),
    INDEX idx_telemetry_device_ts (device, ts_utc) 
);

CREATE TABLE events (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    ts_utc DATETIME(3) NOT NULL,
    device VARCHAR(32) NOT NULL,
    topic VARCHAR(255) NOT NULL,
    kind VARCHAR(16) NOT NULL,   
    payload TEXT NOT NULL,
    PRIMARY KEY (id),
    INDEX idx_events_device_ts (device, ts_utc)
);

CREATE USER 'iot'@'localhost' IDENTIFIED BY 'iot';
GRANT ALL PRIVILEGES ON iot_b3.* TO 'iot'@'localhost';
FLUSH PRIVILEGES;