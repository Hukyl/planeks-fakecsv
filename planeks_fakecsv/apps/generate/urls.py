from django.urls import path

from . import views

app_name = 'gen'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_schema, name='create'),
    path('<int:schema_id>/edit/', views.edit_schema, name='edit'),
    path('<int:schema_id>/delete/', views.delete_schema, name='delete'),
    path('<int:schema_id>/datasets/', views.list_datasets, name='datasets'),
    path(
        '<int:schema_id>/datasets/create/',
        views.create_dataset, name='create-dataset'
    ),
]
