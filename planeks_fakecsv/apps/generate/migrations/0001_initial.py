# Generated by Django 4.0.5 on 2022-06-04 08:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSchema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('column_delimiter', models.CharField(choices=[(',', 'Comma (,)'), ('|', 'Pipe (|)'), (';', 'Semicolon (;)'), ('\t', 'Tab (\\t)')], default=',', max_length=1)),
                ('string_character', models.CharField(choices=[("'", "Single-quote (')"), ('"', 'Double-quote (")')], default='"', max_length=1)),
                ('last_modified_at', models.DateField(auto_now=True)),
                ('schema_columns', models.JSONField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schemas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
