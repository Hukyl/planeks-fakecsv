from __future__ import annotations

from django.db import models
from django.contrib.auth import get_user_model


class DataSchema(models.Model):
    """Data schema to generate fake CSV data according to it"""

    class ColumnDelimiter(models.TextChoices):
        """Column value separator in CSV file"""
        COMMA = ',', 'Comma (,)'
        PIPE = '|', 'Pipe (|)'
        SEMICOLON = ';', 'Semicolon (;)'
        TAB = '\t', 'Tab (\\t)'

    class StringCharacter(models.TextChoices):
        """String defining character in CSV file"""
        SINGLE_QUOTE = '\'', 'Single-quote (\')'
        DOUBLE_QUOTE = '"', 'Double-quote (")'

    name = models.CharField(max_length=50, null=False, blank=False)
    column_delimiter = models.CharField(
        max_length=1, choices=ColumnDelimiter.choices, null=False,
        blank=False, default=ColumnDelimiter.COMMA
    )
    string_character = models.CharField(
        max_length=1, choices=StringCharacter.choices, null=False,
        blank=False, default=StringCharacter.DOUBLE_QUOTE
    )
    last_modified_at = models.DateField(auto_now=True)
    columns = models.JSONField(null=False, blank=False)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE,
        related_name='schemas', null=False
    )


def user_directory_path(instance: DataSet, filename: str) -> str:
    """
    Upload path transformation for `DataSet.csv_file`

    Args:
        instance (DataSet)
        filename (str)

    Returns:
        str
    """
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.schema.user.id}/{filename}'


class DataSet(models.Model):
    """
    Data set, storing created csv file according to schema
    """

    schema = models.ForeignKey(
        DataSchema, on_delete=models.CASCADE,
        related_name='datasets', null=False
    )
    csv_file = models.FileField(upload_to=user_directory_path)
    created_at = models.DateField(auto_now_add=True)
