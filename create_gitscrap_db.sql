-- Database: augur

-- DROP DATABASE IF EXISTS augur;

CREATE DATABASE gitscrap
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF8'
    LC_CTYPE = 'en_US.UTF8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

GRANT ALL ON DATABASE gitscrap TO scraping;

GRANT ALL ON DATABASE gitscrap TO postgres;

GRANT TEMPORARY, CONNECT ON DATABASE gitscrap TO PUBLIC;