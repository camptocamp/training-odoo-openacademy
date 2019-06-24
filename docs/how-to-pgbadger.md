<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
Please propose your modification on
https://github.com/camptocamp/odoo-template instead.
-->
# How to use pgBadger to optimize database queries

This guide assumes you have a local database running.
It explains how to extract logs and feed them to pgBadger then you can find slow queries or other database issues.

## Extract logs

1. Configure PostgreSQL to generate logs to analyze, log in the database

  ```
  $ docker-compose run --rm odoo psql
  ```
  And run the following `ALTER SYSTEM` commands:

  ```
  ALTER SYSTEM SET log_min_duration_statement = '0';
  ALTER SYSTEM SET log_line_prefix = '%t [%p]: [%l-1] ';
  ALTER SYSTEM SET log_checkpoints = 'on';
  ALTER SYSTEM SET log_connections = 'on';
  ALTER SYSTEM SET log_disconnections = 'on';
  ALTER SYSTEM SET log_lock_waits = 'on';
  ALTER SYSTEM SET log_temp_files = '0';
  ALTER SYSTEM SET log_autovacuum_min_duration = '0';
  ALTER SYSTEM SET log_error_verbosity = 'default';
  ```

2. Restart the db container

  ```
  $ docker-compose restart db
  ```

3. At this point, PostgreSQL generates a lot of logs. This is the time to log into Odoo and do the actions you want to analyze.

4. Extract the odoo logs to a local file that will be feeded to pgBadger.

  ```
  $ mkdir -p logs/out
  $ docker logs --since=2017-04-26T10:37:00.000000000Z <project>_db_1 2> logs/logs.txt
  ```
  Note: the time here is UTC, you can prefer to use your local time such as: `2017-04-26T12:37:00.000000000+02:00`

5. Generate the pgBadger analysis and open it in a browser

  ```
  $ docker run --rm -v "$(pwd)/logs:/logs" -v "$(pwd)/logs/out:/data" uphold/pgbadger /logs/logs.txt
  $ xdg-open logs/out/out.html
  ```
