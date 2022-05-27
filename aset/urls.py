from django.urls import path
from .views import *

app_name = 'aset'

urlpatterns = [
    path('', menu_buat_aset, name='menu_buat_aset'),
    path('view', menu_lihat_aset, name='menu_lihat_aset'),
    path('hewan_menghasilkan_produk_hewan', hewan_menghasilkan_produk_hewan, name='hewan_menghasilkan_produk_hewan'),
    path('bibit_menghasilkan_panen', bibit_menghasilkan_panen, name='bibit_menghasilkan_panen'),
    path('cdekor', create_dekorasi, name='create_dekor'),
    path('udekor', update_dekorasi, name='update_dekor'),
    path('list-dekorasi', read_dekorasi, name='list_dekorasi'),
    path('cbibit', create_bibit_tanaman, name='create_bibit'),
    path('ubibit', update_bibit, name='update_bibit'),
    path('list-bibit-tanaman', read_bibit_tanaman, name='list_bibit_tanaman'),
    path('ckandang', create_kandang, name='create_kandang'),
    path('ukandang', update_kandang, name='update_kandang'),
    path('list-kandang', read_kandang, name='list_kandang'),
    path('chewan', create_hewan, name='create_hewan'),
    path('uhewan', update_hewan, name='update_hewan'),
    path('list-hewan', read_hewan, name='list_hewan'),
    path('calatproduksi', create_alat, name='create_alat'),
    path('ualatproduksi', update_alat, name='update_alat'),
    path('list-alat-produksi', read_alat, name='list_alat'),
    path('cpetak', create_petak, name='create_petak'),
    path('upetak', update_petak, name='update_petak'),
    path('list-petak', read_petak, name='list_petak'),
    path('delete', delete_aset, name='delete'),
]

