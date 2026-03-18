-- urie 1
SELECT * FROM telemetry ORDER BY ts_utc DESC LIMIT 10;

-- query 2
SELECT * FROM events ORDER BY ts_utc DESC LIMIT 10;

-- query 3
SLECT * FROM telemetry
WHERE ts_utc > (NOW() - INTERVAL 1 HOUR) ORDER BY ts_utc DESC;

-- query 4
SELECT * FROM telemetry
WHERE sensor_id = 'temp_sensor_1' ORDER BY value DESC LIMIT 10;

-- query 5
SELECT * FROM telemetry
ORDER BY value ASC LIMIT 10;

-- queries 6
DELETE FROM telemetry;
DELETE FROM events;