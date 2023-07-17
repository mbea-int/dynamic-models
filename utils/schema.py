from copy import copy

from django.apps import apps
from django.db import migrations, models
from django.db.backends.base import schema
from django.db import connections

class SchemaEditor(object):
    """The class that holds the appropriate functions for the creation and update of migrations for
    dynamic models."""

    def create_model(self, dynamic_model, fields):

        # Get the app label and model name
        app_label = dynamic_model._meta.app_label
        model_name = dynamic_model.__name__

        # Create a dictionary to store the new field names and types
        field_dict = {}

        # Loop through the fields and build the field dictionary
        for field_data in fields:
            field_name = field_data['name']
            field_type = field_data['type']

            if field_type == 'string':
                field_instance = models.CharField(max_length=255)
            elif field_type == 'number':
                field_instance = models.DecimalField(max_digits=10, decimal_places=2)
            elif field_type == 'boolean':
                field_instance = models.BooleanField()

            field_dict[field_name] = field_instance

        # Create a new model with the fields
        # new_model = type(model_name, (models.Model,), field_dict)

        # Get the database connection alias from the dynamic_model's objects
        db_alias = dynamic_model.objects.db

        # Use a custom app registry to temporarily register the new model
        custom_apps = copy(apps)
        custom_apps.all_models[app_label][model_name.lower()] = dynamic_model

        # Create a migration to add the new fields
        operations = []
        for field_name, field_instance in field_dict.items():
            operations.append(migrations.AddField(
                model_name,
                field_name,
                field_instance,
                preserve_default=False,
            ))

        # Create the migration
        migration = migrations.Migration(app_label, operations)

        # Get the executor for the database connection and apply the migration
        with connections[db_alias].schema_editor() as schema_editor:
            executor = migrations.executor.MigrationExecutor(connections[db_alias])
            executor.loader.check_consistent_history(connections[db_alias])
            # Get the migration state from the executor.loader
            migration_state = executor.loader.project_state()

            # Apply the migration to the database
            migration.apply(schema_editor, migration_state)

            # Update the database schema for the new model
            # Update the database schema for the new model
            with schema_editor:
                schema_editor.create_model(dynamic_model)
                for sql in schema_editor.deferred_sql:
                    schema_editor.execute(sql)

        # Unregister the new model from the custom app registry
        del custom_apps.all_models[app_label][model_name.lower()]

        # Register the new model in the app's registry
        apps.all_models = custom_apps.all_models
        apps.all_models[app_label][model_name.lower()] = dynamic_model

    def update_model(self, dynamic_model, fields):
       pass