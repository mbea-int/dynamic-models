from django.contrib import admin

from api.models import create_dynamic_model

# Register your models here.

site = admin.site
model = create_dynamic_model(model_name="tabela1", fields={})

for reg_model in site._registry.keys():
    if model._meta.db_table == reg_model._meta.db_table:
        del site._registry[reg_model]

# Try the regular approach too, but this may be overdoing it
try:
    site.unregister(model)
except Exception:
    pass