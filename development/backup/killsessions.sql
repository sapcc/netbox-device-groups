SELECT pg_terminate_backend(pid)
  FROM pg_stat_activity
WHERE pid <> pg_backend_pid()
  AND datname = 'netbox' ;
DROP DATABASE netbox;
CREATE DATABASE netbox;
