from django.urls import path
from . import views

app_name = 'lumbung'

urlpatterns = [
    path('', views.list_transaksi_upgrade_lumbung, name='list_transaksi_upgrade_lumbung'),
    path('upgrade-lumbung', views.upgrade_lumbung, name='upgrade_lumbung')
]
