# pylint: disable=E1101

from faker import Faker
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from .models import DataSchema, DataSet


faker = Faker()
CSV_DATA_TYPES = {
    'Full name': faker.name,
    'Job': faker.job,
    'Domain name': faker.domain_name,
    'Phone number': faker.msisdn,  # in GSM
    'Company name': faker.company,
    'Address': lambda: faker.address().replace('\n', '; '),
    'Date': faker.date
}


@login_required
def index(request: HttpRequest) -> HttpResponse:
    schemas = DataSchema.objects.filter(user=request.user)
    return render(
        request, 'generate/index.html', context={'schemas': schemas}
    )


@require_http_methods(["GET", "POST"])
@login_required
def create_schema(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, 'generate/create_schema.html', context={
            'column_delimiters': DataSchema.ColumnDelimiter.choices,
            'string_characters': reversed(DataSchema.StringCharacter.choices),
            'column_types': CSV_DATA_TYPES.keys()
        })
    q = request.POST.dict()
    q.pop('csrfmiddlewaretoken')
    schema = DataSchema(
        name=q.pop('name'), column_delimiter=q.pop('column_delimiter'),
        string_character=q.pop('string_character'), user=request.user
    )
    schema_json = {'schema': []}
    for i in range(len(q) // 3):
        column = int([
            k for k in q if q[k] == str(i)
        ][0].removesuffix('__order'))
        name = q.get(f'{column}__name')
        csv_type = q.get(f'{column}__type')
        schema_json['schema'].append({'name': name, 'type': csv_type})
    schema.columns = schema_json
    schema.save()
    return redirect(reverse('gen:index'))
