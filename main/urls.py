from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.login, name='login'),
    path('home', views.home, name = 'home'),
    path('logout', views.logout, name = 'logout'),
    path('produk', views.produk, name = 'produk'),
    path('produksi', views.produksi, name = 'produksi'),
    path('histori_produk_makanan', views.histori_produk_makanan, name = 'histori_produk_makanan'),
    path('lihat_isi_lumbung', views.lihat_isi_lumbung, name = 'lihat_isi_lumbung'),
    path('produksi/<slug:slug>', views.produksi_details, name = 'produk_details'),
    path('update_produksi/<slug:slug>', views.update_produksi, name = 'update_produksi'),
    path('delete_produksi/<slug:slug>', views.delete_produksi, name = 'delete_produksi'),
    path('create_produk', views.create_produk, name = 'create_produk'),
    path('create_produk/<slug:slug>', views.update_produk, name = 'update_produk'),
    path('delete_produk/<slug:slug>', views.delete_produk, name = 'delete_produk'),
    path('create_produksi', views.create_produksi, name = 'create_produksi'),
    path('create_histori_produk_makanan', views.create_histori_produk_makanan, name = 'create_histori_produk_makanan'),
    path('register_pengguna', views.register_pengguna, name = 'register_pengguna'),  
    path('register_admin', views.register_admin, name = 'register_admin')
]
