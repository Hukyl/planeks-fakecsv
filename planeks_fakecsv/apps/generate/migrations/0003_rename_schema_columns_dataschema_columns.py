# Generated by Django 4.0.5 on 2022-06-04 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generate', '0002_dataset'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dataschema',
            old_name='schema_columns',
            new_name='columns',
        ),
    ]