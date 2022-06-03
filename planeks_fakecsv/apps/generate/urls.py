from django.urls import path

from . import views

app_name = 'gen'
urlpatterns = [
    path('', views.index, name='index'),
]
