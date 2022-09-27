psql --username=postgres --no-password --command="CREATE DATABASE OSSPackRat;"
psql --username=postgres --no-password --dbname=OSSPackRat --file=create_tables.sql
