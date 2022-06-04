from django.urls import path

from . import views

app_name = 'gen'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_schema, name='create'),
    path('edit/<int:schema_id>/', views.edit_schema, name='edit'),
    path('delete/<int:schema_id>/', views.delete_schema, name='delete'),
]
