"""
This module provides with models and classes for `generate` app.

Classes:
    - CSVValueGenerator: generator of fake csv values based on data schema
    - DataSchema: schema to store JSON column schema
    - DataSet: data set to store created CSV file based
        on corresponding data schema
"""

from __future__ import annotations

from datetime import datetime
from io import BytesIO
from typing import Generator

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import models
from faker import Faker


class CSVValueGenerator:
    """CSV value generator, according to `DataSchema`."""

    DATA_TYPES = (
        'full_name', 'job', 'domain_name', 'phone_number',
        'company_name', 'address', 'date'
    )

    def __init__(self, schema: DataSchema):
        self.schema = schema
        self.faker = Faker()

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        """
        Get Django-like choices for data types

        Returns:
            list[tuple[str, str]]: (value, representation)
        """
        return [
            (dtype, dtype.replace('_', ' ').title())
            for dtype in cls.DATA_TYPES
        ]

    def _string_wrap(self, value: str) -> str:
        return (
            self.schema.string_character +
            value +
            self.schema.string_character
        )

    def full_name(self) -> str:
        """
        Get random full name, wrapped in schema string character

        Returns:
            str
        """
        return self._string_wrap(self.faker.name())

    def job(self) -> str:
        """
        Get random job, wrapped in schema string character

        Returns:
            str
        """
        return self._string_wrap(self.faker.job())

    def domain_name(self) -> str:
        """
        Get random domain name

        Returns:
            str
        """
        return self.faker.domain_name()

    def phone_number(self) -> str:
        """
        Get random GSM phone number

        Returns:
            str
        """
        return self.faker.msisdn()

    def company_name(self) -> str:
        """
        Get random company name, wrapped in schema string character

        Returns:
            str
        """
        return self._string_wrap(self.faker.company())

    def address(self) -> str:
        """
        Get random address, wrapped in schema string character

        Returns:
            str
        """
        return self._string_wrap(self.faker.address().replace('\n', ', '))

    def date(self) -> str:
        """
        Get random date between Jan 1, 1970 and now

        Returns:
            str
        """
        return self.faker.date()

    def __getitem__(self, item: str) -> str:
        """
        Get random value of `item` type.
        See `DATA_TYPES` to be passed as `item`

        Args:
            item (str): type of data

        Returns:
            str
        """
        return getattr(self, item)()

    def generate(self, *, num_rows: int) -> Generator[str]:
        """
        Yield csv file rows, separating values with schema column delimiter

        Args:
            num_rows (int): number of rows of fake data to be yielded

        Yields:
            str
        """
        if num_rows < 1:
            raise ValueError('at least one row should be created')
        names = [x['name'] for x in self.schema.columns.get('schema')]
        csv_types = [x['type'] for x in self.schema.columns.get('schema')]
        sep = self.schema.column_delimiter
        yield sep.join(names) + '\n'
        for _ in range(num_rows):
            yield sep.join(self[csv_type] for csv_type in csv_types) + '\n'



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


class DataSet(models.Model):
    """
    Data set, storing created csv file according to schema
    """

    schema = models.ForeignKey(
        DataSchema, on_delete=models.CASCADE,
        related_name='datasets', null=False
    )
    csv_file = models.FileField()
    created_at = models.DateField(auto_now_add=True)

    def update_csv(self, *, num_rows: int) -> True:
        """
        Update data set according to the columns.

        Args:
            num_rows (int): number of rows of fake data

        Returns:
            DataSet
        """
        # pylint: disable=no-member
        generator = CSVValueGenerator(self.schema)
        with BytesIO() as buffer:
            for line in generator.generate(num_rows=num_rows):
                buffer.write(line.encode('utf-8'))
            self.csv_file.save(
                (
                    f"{self.schema.id}__{datetime.now():%Y-%m-%d-%H-%M-%S}"
                    ".csv"
                ),
                ContentFile(buffer.getbuffer())
            )
        return True
