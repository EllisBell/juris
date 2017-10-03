DROP TABLE acordao_descritor;
DROP TABLE acordao;

CREATE TABLE acordao (
id		 		    serial CONSTRAINT acordao_pk PRIMARY KEY,
processo 		    varchar,
tribunal_id         integer REFERENCES tribunal(id),
num_convencional    varchar,
relator  		    varchar,
numero   	        varchar,
data 	 		    date,
votacao  	        varchar,
trib_recorrido      varchar, -- também "Tribunal Recurso" - ver http://www.dgsi.pt/jtrc.nsf/8fe0e606d8f56b22802576c0005637dc/5b4178016c32ce2a802581a3003e4845?OpenDocument
proc_trib_recorrido varchar,
data_dec_recorrida  date, -- http://www.dgsi.pt/jtrp.nsf/56a6e7121657f91e80257cda00381fdf/b63635f2cdffa64280256aed004593bf?OpenDocument
txt_integral_flag   varchar,
txt_parcial_flag    varchar,
privacidade         integer,
meio_processual     varchar,
decisao			    varchar,
indic_eventuais     varchar,
area_tematica       varchar,-- http://www.dgsi.pt/jtrp.nsf/56a6e7121657f91e80257cda00381fdf/aa677fb005b0c4078025686b00670104?OpenDocument
legis_nacional      varchar, -- see above
juris_nacional      varchar, -- see above
sumario	 		    varchar,
txt_parcial 	    varchar,
txt_integral 	    varchar,
html_txt_integral   varchar,
url                 varchar
)

CREATE TABLE acordao_descritor (
acordao_id integer REFERENCES acordao(id),
descritor  varchar
)


-- to run this file in psql: \i ''C:\Users/Tom/ProgStuff/Projects/juris/sql_dev/acordao.sql'