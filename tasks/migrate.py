# -*- coding: utf-8 -*-
# This file has been generated with 'invoke project.sync'.
# Do not modify. Any manual change will be lost.
# Please propose your modification on
# https://github.com/camptocamp/odoo-template instead.
# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import fnmatch
import os
import shutil
from pprint import pprint

from invoke import task

from .common import (
    GIT_IGNORES,
    TEMPLATE_GIT,
    TEMPLATE_GIT_REPO_URL,
    ask_or_abort,
    cd,
    cookiecutter_context,
    git_ignores_global,
    tempdir,
)
from .database import execute_db_request, get_db_list, get_db_request_result
from .project import _exclude_fnmatch, sync

try:
    from cookiecutter.main import cookiecutter
except ImportError as e:
    print('Missing cookiecutter from requirements')
    print('Please run `pip install -r tasks/requirements.txt`')
    raise e


def _move_specifc_addons_to_local_src(ctx, specific_addon_paths_to_keep):
    print('Move modules to odoo/local-src:')
    modules_to_move = []
    for path in specific_addon_paths_to_keep.split(','):
        files = os.listdir(path)
        for f in files:
            print('* {}'.format(f))
            modules_to_move.append((path, f))

    ask_or_abort(
        "These modules will be moved into odoo/local-src."
        " Are you sure it's correct?"
    )

    for path, module in modules_to_move:
        shutil.move(
            os.path.join(path, module), os.path.join('odoo/local-src/', module)
        )

    ctx.run('git add .')
    msg = 'Move specific addons to odoo/local-src'
    ctx.run('git commit -m "{}" -e -vv'.format(msg), pty=True)


def _prepare_files_and_dirs(ctx, paths_to_keep):
    # Determine files/directories to keep in current version
    files_directories_to_keep = (
        ['./.git'] + GIT_IGNORES + git_ignores_global(ctx)
    )
    if paths_to_keep:
        for path in paths_to_keep.split(','):
            files_directories_to_keep.append('./%s' % path)
    # TODO: Optimize following loops
    for file_to_keep in files_directories_to_keep:
        if file_to_keep.endswith('/*'):
            files_directories_to_keep.append(file_to_keep[:-2])
    for file_to_keep in files_directories_to_keep:
        if file_to_keep.endswith('/'):
            files_directories_to_keep.append(file_to_keep[:-1])
    for file_to_keep in files_directories_to_keep:
        if not file_to_keep.startswith('./'):
            files_directories_to_keep.append('./%s' % file_to_keep)

    # Determine files/directories to delete in current version
    files_to_delete = []
    directories_to_delete = []
    for root, dirs, files in os.walk('.', topdown=True):
        if files_directories_to_keep:
            dirs[:] = _exclude_fnmatch(root, dirs, files_directories_to_keep)
            files[:] = _exclude_fnmatch(root, files, files_directories_to_keep)
        files_to_delete.extend([os.path.join(root, f) for f in files])
        directories_to_delete.extend([os.path.join(root, d) for d in dirs])

    # Be sure that we will not delete parent directories.
    # Example if we want to keep odoo/local-src/, we don't want to remove odoo/
    for directory in directories_to_delete:
        for file_to_keep in files_directories_to_keep:
            if file_to_keep.startswith(directory):
                directories_to_delete.remove(directory)
                break

    # Ask confirmation for deleted files
    print('Removing files:')
    for path in files_to_delete:
        print('* {}'.format(path))

    ask_or_abort("These files will be deleted. Are you sure it's correct?")

    # Ask confirmation for deleted directories
    print('Removing directories:')
    for directory in directories_to_delete:
        print('* {}'.format(directory))

    ask_or_abort(
        "These directories will be deleted. Are you sure it's correct?"
    )

    # Return list of files/directories needed into main function
    return files_directories_to_keep, files_to_delete, directories_to_delete


def _prepare_files_to_sync_from_odoo_template(
    tmp, files_directories_to_keep, version=None, fork=None, fork_url=None
):
    # Get new version from odoo-template and determine files to synchronize
    git_repo = TEMPLATE_GIT
    if fork:
        # use different remote
        git_repo = TEMPLATE_GIT_REPO_URL.format(fork)
    elif fork_url:
        git_repo = fork_url
    if fork or fork_url:
        print('Using fork:', git_repo)

    try:
        cc_context = cookiecutter_context()
        # To avoid to have current version as default
        del cc_context['odoo_version']
        cc_context['migration'] = 'yes'
    except FileNotFoundError:
        cc_context = False

    template = cookiecutter(
        git_repo,
        checkout=version,
        extra_context=cc_context,
        output_dir=tmp,
        overwrite_if_exists=True,
    )

    selected_files = set()
    with cd(template):
        include = []
        for path in os.listdir(template):
            if os.path.isfile(os.path.join(template, path)):
                include.append('./%s' % path)
            else:
                include.append('./%s/*' % path)

        # We want to synchronize all files from odoo-template
        for root, dirs, files in os.walk('.', topdown=True):
            if files_directories_to_keep:
                files[:] = _exclude_fnmatch(
                    root, files, files_directories_to_keep
                )
            syncfiles = [os.path.join(root, f) for f in files]
            for incl in include:
                selected_files.update(fnmatch.filter(syncfiles, incl))

        # Ask confirmation for files to synchronize
        print('Syncing files:')
        for s in sorted(selected_files):
            print('* {}'.format(s))

        ask_or_abort(
            "These files will be synchronized." "Are you sure it's correct?"
        )

    # Get specific modules from odoo-template
    new_modules = []
    for selected_file in selected_files:
        if selected_file.startswith('./odoo/local-src/'):
            module_path = './odoo/local-src/%s' % selected_file.split('/')[3]
            if module_path not in new_modules:
                new_modules.append(module_path)

    # Ask confirmation before override specific modules
    print('Modules to override:')
    for s in sorted(new_modules):
        print('* {}'.format(s))

    ask_or_abort(
        "These modules will be entirely overridden. "
        "Are you sure it's correct?"
    )

    return selected_files, template, new_modules


def _do_convert_project(
    ctx,
    files_to_delete,
    directories_to_delete,
    new_modules,
    selected_files,
    template,
):
    # Remove files into current version
    for path in files_to_delete:
        os.remove(path)

    # Remove directories into current version
    for directory in directories_to_delete:
        shutil.rmtree(directory, ignore_errors=True)

    # Remove specific modules into current version to override
    for new_module in new_modules:
        shutil.rmtree(new_module, ignore_errors=True)

    # Synchronize files from new version
    for relpath in selected_files:
        source = os.path.join(template, relpath)
        target_dir = os.path.dirname(relpath)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        shutil.copy(source, relpath)

    # Commit the project conversion
    new_cc_context = cookiecutter_context()
    ctx.run('git add .')
    msg = 'Convert project to new version: {}'.format(
        new_cc_context['odoo_version']
    )
    ctx.run('git commit -m "{}" -e -vv'.format(msg), pty=True)


def _get_old_module_list(new_modules):
    # Get old specific modules
    old_modules = []
    local_modules = sorted(
        [
            './odoo/local-src/%s' % d
            for d in os.listdir('./odoo/local-src/')
            if os.path.isdir('./odoo/local-src/%s' % d)
        ]
    )
    for local_module in local_modules:
        if local_module not in new_modules:
            old_modules.append(local_module)
    return old_modules


def _rename_manifest_for_all_modules(ctx, old_modules):
    # Ask confirmation before rename manifest in specific modules
    print('Renaming manifest on modules:')
    for s in sorted(old_modules):
        print('* {}'.format(s))

    ask_or_abort(
        "Manifest will be renamed (if needed) on these modules. "
        "Are you sure it's correct?"
    )

    # Rename manifest files
    need_to_commit = False
    for old_module in old_modules:
        if os.path.isfile('%s/__openerp__.py' % old_module):
            if not os.path.isfile('%s/__manifest__.py' % old_module):
                os.rename(
                    '%s/__openerp__.py' % old_module,
                    '%s/__manifest__.py' % old_module,
                )
                need_to_commit = True

    # Commit the renaming of manifest
    if need_to_commit:
        ctx.run('git add .')
        msg = 'Rename manifest for old modules'
        ctx.run('git commit -m "{}" -e -vv'.format(msg), pty=True)


def _make_old_modules_uninstallables(ctx, old_modules):
    # Ask confirmation before rename manifest in specific modules
    print('Make uninstallable on modules:')
    for s in sorted(old_modules):
        print('* {}'.format(s))

    ask_or_abort(
        "These modules will be defined uninstallables (if needed). "
        "Are you sure it's correct?"
    )

    # Make old modules uninstallable
    need_to_commit = False
    for old_module in old_modules:
        if os.path.isfile('%s/__manifest__.py' % old_module):
            sed_cmd = r"""sed -i -e "s/\"/'/g" -e "/^[ ]*\('installable':\).*/{s//\1 False,/;:a;n;ba;q}" -e "$a s/}/    'installable': False,\n}/" """  # noqa: E501
            file = ' {old_module}/__manifest__.py'.format(
                old_module=old_module
            )
            ctx.run(sed_cmd + file)
            need_to_commit = True

    # Commit the uninstallable modules
    if need_to_commit:
        ctx.run('git add .')
        msg = 'Make old modules uninstallable'
        ctx.run('git commit -m "{}" -e -vv'.format(msg), pty=True)


@task(name='convert-project')
def convert_project(
    ctx,
    specific_addon_paths_to_keep='',
    paths_to_keep='',
    version=None,
    fork=None,
    fork_url=None,
):
    """Convert project to new version"""
    # dirty hack to make sure we don't call the cookiecutter post script.
    os.environ["CONVERT_PROJECT"] = "True"
    if specific_addon_paths_to_keep:
        _move_specifc_addons_to_local_src(ctx, specific_addon_paths_to_keep)

    files_directories_to_keep, files_to_delete, directories_to_delete = _prepare_files_and_dirs(
        ctx, paths_to_keep
    )

    with tempdir() as tmp:
        selected_files, template, new_modules = _prepare_files_to_sync_from_odoo_template(
            tmp, files_directories_to_keep, version, fork, fork_url
        )

        _do_convert_project(
            ctx,
            files_to_delete,
            directories_to_delete,
            new_modules,
            selected_files,
            template,
        )

        old_modules = _get_old_module_list(new_modules)
        if old_modules:
            migrate_old_module = input(
                "Rename old manifest and put them uninstallable? [yes/no] : "
            )
            if migrate_old_module.lower() in ['y', 'yes']:
                _rename_manifest_for_all_modules(ctx, old_modules)
                _make_old_modules_uninstallables(ctx, old_modules)
    sync(ctx, version=version, fork=fork, fork_url=fork_url)
    del os.environ["CONVERT_PROJECT"]


@task(name='check-modules')
def check_modules(ctx, migrated_db, full_db, sample_db):
    """Print modules comparison between given databases"""
    can_continue = True
    db_list = get_db_list(ctx)
    if migrated_db not in db_list:
        print("Migrated database `%s` not found" % migrated_db)
        can_continue = False
    if full_db not in db_list:
        print("Full database `%s` not found" % full_db)
        can_continue = False
    if sample_db and sample_db not in db_list:
        print("Sample database `%s` not found" % sample_db)
        can_continue = False

    if can_continue:
        sql = """
            SELECT
                name,
                state
            FROM
                ir_module_module
            WHERE
                state IN ('to install', 'to upgrade', 'installed')
            ORDER BY
                name;
        """
        migrated_modules = get_db_request_result(ctx, migrated_db, sql) or []
        full_modules = get_db_request_result(ctx, full_db, sql) or []
        sample_modules = get_db_request_result(ctx, sample_db, sql) or []

        print('')
        print('Modules in migrated database:')
        pprint(set(migrated_modules))

        print('')
        print('Modules in full database:')
        pprint(set(full_modules))

        print('')
        print('Modules in migrated database, but not in full database:')
        # In migrated database,
        # we get "to install", "to update" and  "installed" modules
        #
        # In full database, we only get "installed" modules
        #
        # So we just compare modules name without their state
        pprint({x[0] for x in migrated_modules} - {x[0] for x in full_modules})

        print('')
        print('Modules in full database, but not in sample database:')
        pprint(set(full_modules) - set(sample_modules))

        print('')
        print('Modules in sample database, but not in full database:')
        pprint(set(sample_modules) - set(full_modules))


@task(name='reduce-db-size')
def reduce_db_size(ctx, database_name, date):
    """Remove data (sale order, invoice, ...) in past to have lower database"""
    db_list = get_db_list(ctx)
    if database_name not in db_list:
        print("Database `%s` not found" % database_name)
        return

    # Following file contains all tables to clean
    tables_file = open('tasks/migrate_reduce_db_size_tables.txt', 'r')
    tables_to_clean = tables_file.read().split('\n')

    for table_to_clean in tables_to_clean:
        print('Clean table: %s' % table_to_clean)

        try:
            sql = """
                SELECT COUNT(*) FROM {} WHERE create_date < '{}';
            """.format(
                table_to_clean, date
            )
            record_count = get_db_request_result(ctx, database_name, sql) or []
        except Exception:
            print("==> Table %s doesn't exist" % table_to_clean)
            continue

        sql = """
            ALTER TABLE {} DISABLE TRIGGER ALL;
            DELETE FROM {} WHERE create_date < '{}';
            ALTER TABLE {} ENABLE TRIGGER ALL;
        """.format(
            table_to_clean, table_to_clean, date, table_to_clean
        )
        execute_db_request(ctx, database_name, sql)
        print(
            "==> Clean table {}: {} deleted".format(
                table_to_clean, record_count[0][0]
            )
        )

    print("Launch VACUUM manually: VACUUM FULL ANALYZE;")
