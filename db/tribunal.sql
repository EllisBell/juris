drop table tribunal;

create table tribunal (
id_name     varchar constraint tribunal_pk primary key,
long_name   varchar
)

insert into tribunal(id_name, long_name) values ('TRL', 'Tribunal da Relação de Lisboa');
insert into tribunal(id_name, long_name) values ('TRP', 'Tribunal da Relação do Porto');
insert into tribunal(id_name, long_name) values ('TRC', 'Tribunal da Relação de Coimbra');
insert into tribunal(id_name, long_name) values ('TRE', 'Tribunal da Relação de Évora');
insert into tribunal(id_name, long_name) values ('TRG', 'Tribunal da Relação de Guimarães');


select * from tribunal t;