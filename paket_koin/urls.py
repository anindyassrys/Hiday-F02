from django.urls import path
from . import views

app_name = 'paket_koin'

urlpatterns = [
    path('', views.list_paket_koin, name='list_paket_koin'),
    path('create_paket_koin', views.create_paket_koin, name='create_paket_koin')
]
