DROP TABLE IF EXISTS scooters;

CREATE TABLE scooters (
	id SERIAL PRIMARY KEY,
	company VARCHAR(10),
	last_updated BIGINT,
	bike_id TEXT,
	lat NUMERIC(10,7),
	lon NUMERIC(10,7),
	is_reserved INTEGER,
);



DROP TABLE IF EXISTS clean_log;

CREATE TABLE clean_log (
	id SERIAL PRIMARY KEY,
	clean_time BIGINT,
)

