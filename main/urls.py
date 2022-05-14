from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.login, name='login'),
    path('home', views.home, name = 'home'),
    path('logout', views.logout, name = 'logout'),
    path('produk', views.produk, name = 'produk'),
    path('lihat_isi_lumbung', views.lihat_isi_lumbung, name = 'lihat_isi_lumbung')
]
