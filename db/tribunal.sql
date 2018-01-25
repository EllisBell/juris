drop table tribunal;

-- potentially change this to unique short name, long name (no id)
-- and add primary key
create table tribunal (
id_name     varchar constraint tribunal_pk primary key,
long_name   varchar
)

insert into tribunal(id_name, long_name) values ('TRL', 'Tribunal da Relação de Lisboa');
insert into tribunal(id_name, long_name) values ('TRP', 'Tribunal da Relação do Porto');
insert into tribunal(id_name, long_name) values ('TRC', 'Tribunal da Relação de Coimbra');


select * from tribunal t;