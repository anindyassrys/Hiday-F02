from django.urls import path
from . import views

app_name = 'paket_koin'

urlpatterns = [
    path('', views.list_paket_koin, name='list_paket_koin'),
    path('create-paket-koin', views.create_paket_koin, name='create_paket_koin'),
    path('update-paket-koin/<int:jumlah_koin>/<int:harga>', views.update_paket_koin, name='update_paket_koin'),
    path('list-transaksi-pembelian-koin', views.list_transaksi_pembelian_koin, name='list_transaksi_pembelian_koin'),
    path('create-transaksi-koin/<int:value>/<int:harga>', views.create_transaksi_pembelian_paket_koin, name='create_transaksi_pembelian_paket_koin')
]
