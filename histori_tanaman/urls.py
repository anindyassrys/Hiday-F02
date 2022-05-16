from django.urls import path
from . import views

app_name = 'lumbung'

urlpatterns = [
    path('', views.list_histori_tanaman, name='list_histori_tanaman'),
    path('produksi-tanaman', views.produksi_tanaman, name='produksi_tanaman')
]
