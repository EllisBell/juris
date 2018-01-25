-- index stuff:
-- index on just txt_integral:
create index acordao_idx on acordao using GIN(to_tsvector('tuga', coalesce(txt_integral, '')));

select count(*) from acordao where to_tsvector('tuga', txt_integral) @@ to_tsquery('tuga', 'crime');


-- creating new column with parsed txt of 1 column then create index on that
alter table acordao add column searchable_txt_integral tsvector;

update acordao set searchable_txt_integral =
to_tsvector('tuga', coalesce(txt_integral, '')); -- can concatenate other columns as well

create index txt_search_idx on acordao using GIN(searchable_txt_integral);

-- OR index on tsvector of concatenated columns
create index acordao_idx on acordao using GIN(to_tsvector('tuga', coalesce(txt_integral, '') || '' || coalesce(sumario, '')));
-- Or with weights:
-- TODO test this!
create index acordao_idx on acordao using GIN((setweight(to_tsvector('tuga', coalesce(txt_integral, '')), 'D') ||
setweight(to_tsvector('tuga', coalesce(sumario,'')), 'A'))); -- note extra brackets around expression in GIN function
-- TODO nb. to query this and use index have to do tsvector the same way (e.g. with setweight etc.)
select count(*) from acordao where setweight(to_tsvector('tuga', coalesce(txt_integral, '')), 'D')
|| setweight(to_tsvector('tuga', coalesce(sumario, '')), 'A') @@ to_tsquery('tuga', 'crime');


-- TODO or, much better if confirmed - create index with no weights
-- todo then just pass in the weights to ts_rank
create index acordao_idx on acordao using GIN(to_tsvector('tuga', coalesce(txt_integral, ''))
|| to_tsvector('tuga', coalesce(sumario, '')));

--TODO MORE COLUMNS!
create index acordao_idx on acordao using gin((to_tsvector('tuga', coalesce(txt_integral, ''))
|| to_tsvector('tuga', coalesce(sumario, ''))
|| to_tsvector('tuga', coalesce(processo, ''))
|| to_tsvector('tuga', coalesce(relator, ''))));

select count(*) from acordao where to_tsvector('tuga', coalesce(txt_integral, ''))
|| to_tsvector('tuga', coalesce(sumario, ''))
|| to_tsvector('tuga', coalesce(processo, ''))
|| to_tsvector('tuga', coalesce(relator, '')) @@ to_tsquery('tuga', 'hazelnuts');

-- With rankings, including setting weight to give processo and relator greater importance
select acordao_id, ts_rank_cd(setweight(to_tsvector('tuga', coalesce(txt_integral, '')), 'D')
|| setweight(to_tsvector('tuga', coalesce(sumario, '')), 'C')
|| setweight(to_tsvector('tuga', coalesce(processo, '')), 'A')
|| setweight(to_tsvector('tuga', coalesce(relator, '')), 'A'), to_tsquery('tuga', 'hazelnuts')) as rank
from acordao where to_tsvector('tuga', coalesce(txt_integral, ''))
|| to_tsvector('tuga', coalesce(sumario, ''))
|| to_tsvector('tuga', coalesce(processo, ''))
|| to_tsvector('tuga', coalesce(relator, ''))
@@ to_tsquery('tuga', 'hazelnuts');
-- TODO wait I don't think this actually works; I think it gets the results and then indexes them again
-- todo in the setweights, making it super slow where there are lots of results
-- todo try:
-- 1. recreating index, this time with weights
-- 2. create column with weights and index that

---- CREATING NEW COLUMN
alter table acordao add column searchable_idx_col tsvector;

update acordao set searchable_idx_col = null;

-- TODO this gives us only one value from descritores... fix
update acordao set searchable_idx_col = setweight(to_tsvector('tuga', coalesce(txt_integral, '')), 'D')
|| setweight(to_tsvector('tuga', coalesce(sumario, '')), 'C')
|| setweight(to_tsvector('tuga', coalesce(processo, '')), 'A')
|| setweight(to_tsvector('tuga', coalesce(relator, '')), 'A')
|| setweight(to_tsvector('tuga', coalesce(acd.descritor, '')), 'B')
from acordao_descritor as acd
where acordao.acordao_id = acd.acordao_id;

-- Function to get all descritores for an acordao, concatenated
create function get_concatenated_descritores(p_acordao integer) returns varchar as $$
declare
    v_descritores varchar;
begin
    select string_agg(descritor, ' ')
    into v_descritores
    from acordao_descritor
    where acordao_id = p_acordao;

    return v_descritores;
end
$$ LANGUAGE plpgsql;

-- updating searchable_idx_col (using above function for descritores)
update acordao set searchable_idx_col = setweight(to_tsvector('tuga', coalesce(txt_integral, '')), 'D')
|| setweight(to_tsvector('tuga', coalesce(sumario, '')), 'C')
|| setweight(to_tsvector('tuga', coalesce(processo, '')), 'A')
|| setweight(to_tsvector('tuga', coalesce(relator, '')), 'A')
|| setweight(to_tsvector('tuga', coalesce(get_concatenated_descritores(acordao.acordao_id), '')), 'B')
from acordao_descritor as acd
where acordao.acordao_id = acd.acordao_id;

-- Create the index on searchable_idx_col; This will update automatically when new row inserted/updated;
create index acordao_idx on acordao using gin(searchable_idx_col);

-- TRIGGER for above (using PL/pgSQL)
create function acordao_trigger() returns trigger as $$
begin
    new.searchable_idx_col :=
        setweight(to_tsvector('tuga', coalesce(new.txt_integral, '')), 'D')
        || setweight(to_tsvector('tuga', coalesce(new.sumario, '')), 'C')
        || setweight(to_tsvector('tuga', coalesce(new.processo, '')), 'A')
        || setweight(to_tsvector('tuga', coalesce(new.relator, '')), 'A')
        || setweight(to_tsvector('tuga', coalesce(get_concatenated_descritores(acordao.acordao_id), '')), 'B')
        from acordao_descritor as acd
        where acordao_id = acd.acordao_id;
     return new;
end
$$ LANGUAGE plpgsql;

create trigger tsvectorupdate before insert or update
on acordao for each row execute procedure acordao_trigger();

drop trigger tsvectorupdate on acordao;
drop function acordao_trigger();

-- searching using new column
select acordao_id, ts_rank_cd(searchable_idx_col, query) rank
from acordao, to_tsquery('tuga', 'crime') as query
where searchable_idx_col @@ query order by rank desc limit 10

-- TODO add descritores to indexed column as well!

-- NOTE does index have to be made with coalesce cause django passes coalesce???
-- django seemingly still not using index, or even with index quite slow?
-- solution might be to use raw sql... but not ideal

drop index acordao_idx;


-- ********** unaccent / dictionary stuff: ****************
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