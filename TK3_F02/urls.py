"""TK3_F02 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from main import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('paket-koin/', include('paket_koin.urls', namespace="paket-koin")),
    path('', include('main.urls', namespace="home")),
    path('aset/', include('aset.urls')),
    path('lumbung/', include('lumbung.urls', namespace="lumbung")),
    path('histori-tanaman/', include('histori_tanaman.urls', namespace="histori_tanaman")),
    path('cr-histori-hewan/', include('cr_histori_hewan.urls')),
    path('crud-pesanan/', include('crud_pesanan.urls')),
    path('cr-histori-penjualan/', include('cr_histori_penjualan.urls')),
    path('aset/', include('aset.urls'))
]
