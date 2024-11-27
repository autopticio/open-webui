"""Peewee migrations -- 017_add_environment_id_and_refactoring.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['table_name']            # Return model in current state by name
    > Model = migrator.ModelClass                   # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.run(func, *args, **kwargs)           # Run python function with the given args
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.add_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)
    > migrator.add_constraint(model, name, sql)
    > migrator.drop_index(model, *col_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.drop_constraints(model, *constraints)

"""

from contextlib import suppress

import peewee as pw
from peewee_migrate import Migrator


with suppress(ImportError):
    import playhouse.postgres_ext as pw_pext


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your migrations here."""
    
    migrator.change_fields('chat', created_at=pw.BigIntegerField(),
        updated_at=pw.BigIntegerField())

    migrator.change_fields('tool', id=pw.CharField(max_length=255, unique=True),
        user_id=pw.CharField(max_length=255))

    migrator.add_fields(
        'user',

        EnvironmentID=pw.CharField(max_length=255, null=True))

    migrator.remove_fields('user', 'envFileName', 'autoptic_endpoint', 'autoptic_environment')

    migrator.change_fields('user', serverURL=pw.CharField(max_length=255, null=True),
        accessToken=pw.CharField(max_length=255, null=True),
        serverEndpointID=pw.CharField(max_length=255, null=True))


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your rollback migrations here."""
    
    migrator.add_fields(
        'user',

        envFileName=pw.CharField(max_length=255, null=True),
        autoptic_endpoint=pw.CharField(max_length=255, null=True),
        autoptic_environment=pw.TextField(null=True))

    migrator.remove_fields('user', 'EnvironmentID')

    migrator.change_fields('user', serverURL=pw.TextField(null=True),
        accessToken=pw.TextField(null=True),
        serverEndpointID=pw.TextField(null=True))

    migrator.change_fields('tool', id=pw.TextField(unique=True),
        user_id=pw.TextField())

    migrator.change_fields('chat', created_at=pw.DateTimeField(),
        updated_at=pw.DateTimeField())
