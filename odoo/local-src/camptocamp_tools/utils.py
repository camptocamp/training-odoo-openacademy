# This file has been generated with 'invoke project.sync'.
# Do not modify. Any manual change will be lost.
# Please propose your modification on
# https://github.com/camptocamp/odoo-template instead.
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import logging

from psycopg2 import sql

_logger = logging.getLogger(__name__)


def create_index(cr, index_name, table, expression):
    cr.execute(
        'SELECT indexname FROM pg_indexes WHERE indexname = %s', (index_name,)
    )
    if not cr.fetchone():
        # pylint: disable=sql-injection
        cr.execute(
            sql.SQL('CREATE INDEX {}  ON {} {}').format(
                sql.Identifier(index_name),
                sql.Identifier(table),
                sql.SQL(expression),
            )
        )


def is_postgres_superuser(env):
    env.cr.execute("SHOW is_superuser;")
    superuser = env.cr.fetchone()
    return superuser is not None and superuser[0] == 'on' or False


def trgm_extension_exists(env):
    env.cr.execute(
        """
        SELECT name, installed_version
        FROM pg_available_extensions
        WHERE name = 'pg_trgm'
        LIMIT 1;
    """
    )

    extension = env.cr.fetchone()
    if extension is None:
        return 'missing'

    if extension[1] is None:
        return 'uninstalled'

    return 'installed'


def install_trgm_extension(env):
    extension = trgm_extension_exists(env)
    if extension == 'missing':
        _logger.warning(
            'To use pg_trgm you have to install the '
            'postgres-contrib module.'
        )
    elif extension == 'uninstalled':
        if is_postgres_superuser(env):
            env.cr.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
            return True
        else:
            _logger.warning(
                'To use pg_trgm you have to create the '
                'extension pg_trgm in your database or you '
                'have to be the superuser.'
            )
    else:
        return True
    return False
