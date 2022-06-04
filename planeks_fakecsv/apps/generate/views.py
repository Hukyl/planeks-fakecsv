# pylint: disable=E1101

from faker import Faker
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .models import DataSchema

faker = Faker()
CSV_DATA_TYPES = {
    'Full name': faker.name,
    'Job': faker.job,
    'Domain name': faker.domain_name,
    'Phone number': lambda: f'+{faker.msisdn()}',  # in GSM
    'Company name': faker.company,
    'Address': lambda: faker.address().replace('\n', '; '),
    'Date': faker.date
}


def index(request: HttpRequest) -> HttpResponse:
    schemas = DataSchema.objects.filter(user=request.user)
    return render(
        request, 'generate/index.html', context={'schemas': schemas}
    )
