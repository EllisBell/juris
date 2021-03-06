DROP TABLE acordao_recorrido;
DROP TABLE acordao_descritor;
DROP TABLE acordao;
drop table tribunal;


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
html_txt_parcial    varchar,
html_txt_integral   varchar,
url                 varchar,
date_loaded         timestamp,
descritores         varchar
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

-- test data for testing weightings
insert into acordao(sumario, txt_integral)
values('and the word is hazelnuts', 'nada a ver mesmo')

insert into acordao(sumario, txt_integral)
values('nada a ver mesmo', 'and the word is hazelnuts')

insert into acordao(processo, txt_integral)
values('hazelnuts', 'this has it in the processo')

insert into acordao(relator, txt_integral)
values('hazelnuts', 'this has it in the relator')

insert into acordao(relator, txt_integral)
values('bla blu 2', 'this has it in the relator')


select * from acordao where txt_integral like '%hazelnuts%';

select acordao_id, sumario from acordao order by acordao_id desc;

update acordao set tribunal_id = 'TRP'
where acordao_id = 18220;

select * from acordao where acordao_id = 13546;

select * from acordao order by acordao_id desc limit 10;

select * from acordao where searchable_txt_integral is null
limit 10;

select * from acordao where txt_parcial_flag = 'S' and txt_integral_flag = 'S'
limit 2;

alter table acordao add column html_txt_parcial varchar;

select count(*) from acordao

--where tribunal_id in ('TRL', 'TRP');

select max(date_loaded) from acordao;

select * from acordao where acordao.processo = '336/16.9YHLSB.L1-7';

select * from acordao order by acordao_id desc limit 1;


