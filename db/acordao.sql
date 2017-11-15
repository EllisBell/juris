DROP TABLE acordao_recorrido;
DROP TABLE acordao_descritor;
DROP TABLE acordao;


CREATE TABLE acordao (
acordao_id		    serial CONSTRAINT acordao_pk PRIMARY KEY,
processo 		    varchar,
tribunal_id         varchar REFERENCES tribunal(id_name),
seccao              varchar,--http://www.dgsi.pt/jtca.nsf/170589492546a7fb802575c3004c6d7d/e1cd173243db516180258183003cf652?OpenDocument
num_convencional    varchar,
relator  		    varchar,
numero   	        varchar,
data 	 		    date,
votacao  	        varchar,
aditamento          varchar,--http://www.dgsi.pt/jtca.nsf/170589492546a7fb802575c3004c6d7d/e1cd173243db516180258183003cf652?OpenDocument
trib_recorrido      varchar, -- também "Tribunal Recurso" - ver http://www.dgsi.pt/jtrc.nsf/8fe0e606d8f56b22802576c0005637dc/5b4178016c32ce2a802581a3003e4845?OpenDocument
proc_trib_recorrido varchar, -- também "Processo no Tribunal Recurso"
data_dec_recorrida  date, -- http://www.dgsi.pt/jtrp.nsf/56a6e7121657f91e80257cda00381fdf/b63635f2cdffa64280256aed004593bf?OpenDocument
txt_integral_flag   varchar,
txt_parcial_flag    varchar,
privacidade         integer,
meio_processual     varchar,
recorrente          varchar,--http://www.dgsi.pt/jtcn.nsf/89d1c0288c2dd49c802575c8003279c7/9dae9d2a2192345f802581a80035b8a2?OpenDocument
decisao			    varchar,
indic_eventuais     varchar,
area_tematica       varchar,-- http://www.dgsi.pt/jtrp.nsf/56a6e7121657f91e80257cda00381fdf/aa677fb005b0c4078025686b00670104?OpenDocument
doutrina            varchar,-- see above
legis_nacional      varchar, -- see above
juris_nacional      varchar, -- see above
sumario	 		    varchar,
txt_parcial 	    varchar,
txt_integral 	    varchar,
html_txt_integral   varchar,
url                 varchar,
date_loaded         date
)

CREATE TABLE acordao_descritor (
acordao_desc_id serial CONSTRAINT acordao_desc_pk PRIMARY KEY,
acordao_id integer REFERENCES acordao(acordao_id),
descritor  varchar
)

-- there can also be recorrido 2, 3, etc. probably best to have other table
--http://www.dgsi.pt/jtcn.nsf/89d1c0288c2dd49c802575c8003279c7/9dae9d2a2192345f802581a80035b8a2?OpenDocument
CREATE TABLE acordao_recorrido (
acordao_recorrido_id serial CONSTRAINT acordao_rec_pk PRIMARY KEY,
acordao_id integer REFERENCES acordao(acordao_id),
recorrido varchar)


-- to run this file in psql: \i ''C:\Users/Tom/ProgStuff/Projects/juris/sql_dev/acordao.sql'

select * from acordao;
select * from acordao_recorrido;
select * from acordao_descritor;

delete from acordao_recorrido;
delete from acordao_descritor;
delete from acordao;

select * from django_migrations;
delete from django_migrations

select count(distinct(url)) dist from acordao;

-- index stuff:
-- index on just txt_integral:
create index acordao_idx on acordao using GIN(to_tsvector('portuguese', txt_integral));
create index acordao_idx on acordao using GIN(to_tsvector('tuga', txt_integral));


select count(*) from acordao where to_tsvector('portuguese', txt_integral) @@ to_tsquery('portuguese', 'crime');

-- NOTE does index have to be made with coalesce cause django passes coalesce???
-- django seemingly still not using index, or even with index quite slow?
-- solution might be to use raw sql... but not ideal

drop index acordao_idx;

-- unaccent / dictionary stuff:
-- NOTE: had to to this as unaccent is not there by default in database!
create extension unaccent;

-- creating new text search config to use unaccent + portuguese stem:
create text search configuration tuga (copy = portuguese);
alter text search configuration tuga
alter mapping for hword, hword_part, word
with unaccent, portuguese_stem;

-- but this gives some odd results e.g. ã is converted to ae
-- UPDATE: actually above may be wrong - that was maybe just the way psql was displaying results
-- may be able to change dictionary that unaccent uses..
-- or create a new filter dictionary instead of unaccent e.g. with just
-- á -- a; ã -- a; à -- a; and so on. and test if that works.
-- If a new one is created can compare results when using new one vs when using unaccent;

select 'c', 'ç', to_tsvector('tuga', 'ç');
select to_tsvector('tuga', 'não');

SELECT "acordao"."acordao_id", "acordao"."processo", "acordao"."tribunal_id", "acordao"."seccao", "acordao"."num_convencional", "acordao"."relator", "acordao"."numero", "acordao"."data", "acordao"."votacao", "acordao"."aditamento", "acordao"."trib_recorrido", "acordao"."proc_trib_recorrido", "acordao"."data_dec_recorrida", "acordao"."txt_integral_flag", "acordao"."txt_parcial_flag", "acordao"."privacidade", "acordao"."meio_processual", "acordao"."recorrente", "acordao"."decisao", "acordao"."indic_eventuais", "acordao"."area_tematica", "acordao"."doutrina", "acordao"."legis_nacional", "acordao"."juris_nacional", "acordao"."sumario", "acordao"."txt_parcial", "acordao"."txt_integral", "acordao"."html_txt_integral", "acordao"."url", "acordao"."date_loaded", to_tsvector('tuga', COALESCE("acordao"."txt_integral",'')) AS "search" FROM "acordao" WHERE to_tsvector('tuga', COALESCE("acordao"."txt_integral",'')) @@ (plainto_tsquery('tuga', 'crime')) = true;

-- UPDATE
-- using raw sql in Django seems to be faster for some reason
--  term = 'crime'
-- query = "select acordao_id from acordao where to_tsvector('tuga', coalesce(txt_integral,'')) @@ to_tsquery('tuga', %s)"
-- res = Acordao.objects.raw(query, [term])

-- Anyway:::
-- Plan is - make 1 ts_vector column from all searchable columns (txt_integral, sumario, descritores, relator, etc.)
-- have index on that
-- Have weightings as well
-- integrate it into Django model
-- Search on that through Django ORM. If too slow, try raw
-- OR
-- index on each relevant column
-- search across several columns 