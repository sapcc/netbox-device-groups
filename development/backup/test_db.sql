SELECT COUNT (*)
  from pg_class c
  join pg_namespace s on s.oid = c.relnamespace
 where s.nspname not in ('pg_catalog', 'information_schema')
   and s.nspname not like 'pg_temp%'
   and s.nspname not like 'pg_toast%';
