# pylint: disable=E1101

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import DataSchema, DataSet, CSVValueGenerator


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
            'column_types': CSVValueGenerator.choices()
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


@require_http_methods(["GET", "POST"])
@login_required
def edit_schema(request: HttpRequest, schema_id: int) -> HttpResponse:
    if request.method == "GET":
        return render(request, 'generate/edit_schema.html', context={
            'schema': get_object_or_404(DataSchema, id=schema_id),
            'column_types': CSVValueGenerator.choices()
        })
    q = request.POST.dict()
    q.pop('csrfmiddlewaretoken')
    schema = get_object_or_404(DataSchema, id=schema_id)
    if schema.user != request.user:
        raise PermissionDenied
    schema.name = q.pop('name')
    schema.column_delimiter = q.pop('column_delimiter')
    schema.string_character = q.pop('string_character')
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


@require_http_methods(["GET"])
@login_required
def delete_schema(request: HttpRequest, schema_id: int) -> HttpResponse:
    schema = get_object_or_404(DataSchema, id=schema_id)
    if schema.user != request.user:
        raise PermissionDenied
    schema.delete()
    return redirect(reverse('gen:index'))
