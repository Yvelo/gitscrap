-- Database: gitscrap

DROP DATABASE IF EXISTS gitscrap;

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

DROP TABLE IF EXISTS public.repos;

CREATE TABLE IF NOT EXISTS public.repos
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    repository_id integer,
    node_id character varying(255) COLLATE pg_catalog."default",
    full_name character varying(255) COLLATE pg_catalog."default",
    private boolean,
    owner_id integer,
    owner_login character varying(255) COLLATE pg_catalog."default",
    description character varying(8191) COLLATE pg_catalog."default",
    size integer,
    stargazers_count integer,
    watchers_count integer,
    topics character varying(8191) COLLATE pg_catalog."default",
    visibility character varying(255) COLLATE pg_catalog."default",
    fork boolean,
    forks integer,
    open_issues_count integer,
    network_count integer,
    subscriber_count integer,
    license character varying(255) COLLATE pg_catalog."default",
    collaborators_count integer,
    commits_count integer,
    events_count integer,
    branches_count integer,
    repository_score double precision,
    tag character varying(255) COLLATE pg_catalog."default",
    recorded_on timestamp with time zone
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.repos
    OWNER to scraping;


DROP TABLE IF EXISTS public.users;

CREATE TABLE IF NOT EXISTS public.users
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    login character varying(255) COLLATE pg_catalog."default",
    user_id integer,
    node_id character varying(255) COLLATE pg_catalog."default",
    site_admin boolean,
    type character varying(255) COLLATE pg_catalog."default",
    followers_count integer,
    following_count integer,
    subscriptions_count integer,
    organizations_count integer,
    repos_count integer,
    events_count integer,
    user_score double precision,
    tag character varying(255) COLLATE pg_catalog."default",
    recorded_on timestamp with time zone
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.users
    OWNER to scraping;