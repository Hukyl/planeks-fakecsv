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
    schema_columns = models.JSONField(null=False, blank=False)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE,
        related_name='schemas', null=False
    )
