from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.login, name='login'),
    path('home', views.home, name = 'home'),
    path('logout', views.logout, name = 'logout'),
    path('produk', views.produk, name = 'produk'),
    path('produksi', views.produksi, name = 'produksi'),
    path('histori_produk_makanan', views.histori_produk_makanan, name = 'histori_produk_makanan'),
    path('lihat_isi_lumbung', views.lihat_isi_lumbung, name = 'lihat_isi_lumbung'),
    path('produksi/<slug:slug>', views.produksi_details, name = 'produk_details')
]
