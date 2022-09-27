psql --username=postgres --no-password --command="CREATE DATABASE osspackrat_test;"
psql --username=postgres --no-password --dbname=osspackrat_test --file=create_tables.sql
psql --username=postgres --no-password --dbname=osspackrat_test --file=test_seed_data.sql
