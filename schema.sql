CREATE DATABASE IF NOT EXISTS iot_b3
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci; [cite: 628, 629, 630]

USE iot_b3; [cite: 635]

CREATE TABLE IF NOT EXISTS telemetry (
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

CREATE TABLE IF NOT EXISTS events (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    ts_utc DATETIME(3) NOT NULL,
    device VARCHAR(32) NOT NULL,
    topic VARCHAR(255) NOT NULL,
    kind VARCHAR(16) NOT NULL,   
    payload TEXT NOT NULL,
    PRIMARY KEY (id),
    INDEX idx_events_device_ts (device, ts_utc) [cite: 655, 657]
);