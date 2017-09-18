DROP TABLE acordao_descritor;
DROP TABLE acordao;

CREATE TABLE acordao (
id		 		  serial CONSTRAINT acordao_pk PRIMARY KEY,
processo 		  varchar,
relator  		  varchar,
numero   	      varchar,
data 	 		  date,
votacao  	      varchar,
txt_integral_flag varchar,
txt_parcial_flag  varchar,
meio_processual   varchar,
decisao			  varchar,
sumario	 		  varchar,
txt_parcial 	  varchar,
txt_integral 	  varchar
)

CREATE TABLE acordao_descritor (
acordao_id integer REFERENCES acordao(id),
descritor varchar)

-- todo create table for descritores

-- to run this file in psql: \i ''C:\Users/Tom/ProgStuff/Projects/juris/sql_dev/acordao.sql'