CREATE DATABASE dossierdb ENCODING 'UTF8';

CREATE ROLE dossieruser PASSWORD 'intenserecovery';

alter role dossieruser with login;

grant all privileges on all tables in schema public to dossieruser;

grant all privileges on all sequences in schema public to dossieruser;