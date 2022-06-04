from django.contrib import admin

from .models import DataSchema, DataSet


admin.site.register(DataSchema)
admin.site.register(DataSet)
