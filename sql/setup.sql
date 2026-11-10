\set ON_ERROR_STOP on

SELECT 'CREATE DATABASE notesdb'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'notesdb')
\gexec

\connect notesdb

CREATE TABLE IF NOT EXISTS public.notes (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    body text NOT NULL
);

SELECT 'CREATE ROLE notes_app LOGIN'
WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'notes_app')
\gexec

GRANT CONNECT ON DATABASE notesdb TO notes_app;
GRANT USAGE ON SCHEMA public TO notes_app;
GRANT SELECT, INSERT ON TABLE public.notes TO notes_app;
