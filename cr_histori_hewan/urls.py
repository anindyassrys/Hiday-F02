from django.urls import path

from . import views

app_name = 'cr_histori_hewan'

urlpatterns = [
    path('list-histori-hewan', views.list_histori_hewan, name='list-histori-hewan'),
    path('produksi-hewan', views.produksi_hewan, name='create-histori-hewan')
]