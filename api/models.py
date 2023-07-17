from django.db import models

# Create your models here.

def create_dynamic_model(model_name, fields):
    """ Function that helps for the creation of the dynamic model.
     Input
     model_name, type str
     The name of the dynamic model/table
     fields, type list
     The list of dictionaries that contains the columns of the model. Each dictionary in the list
     contains key value pair for name and type of the column.

     Returns
     dynamic_model, type models.Model
     The dynamically created model
     """
    attrs = {'__module__': __name__}
    for field in fields:
        field_name = field['name']
        field_type = field['type']
        if field_type == 'string':
            attrs[field_name] = models.CharField(max_length=255, default="")
        elif field_type == 'number':
            attrs[field_name] = models.DecimalField(max_digits=10, decimal_places=2, default=0)
        elif field_type == 'boolean':
            attrs[field_name] = models.BooleanField(default=False)

    dynamic_model = type(model_name, (models.Model,), attrs)

    # Save the dynamically created model information to the ModelSchema
    dynamic_table, created = ModelSchema.objects.get_or_create(table_name=model_name)

    return dynamic_model

class ModelSchema(models.Model):
    """ The names of the created models/tables are saved here. """
    table_name = models.CharField(max_length=255)

    def __str__(self):
        return self.table_name


class DynamicModelBase(models.Model):
    """ Abstract class that helps in the modification of dynamic models """
    class Meta:
        abstract = True

