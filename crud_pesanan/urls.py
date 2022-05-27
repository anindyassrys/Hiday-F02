from django.urls import path

from . import views

app_name = 'crud_pesanan'

urlpatterns = [
    path('list-pesanan', views.list_histori_pesanan, name='list-pesanan'),
    path('create-pesanan', views.create_pesanan, name='create-pesanan'),
    path('detail/<str:id>/', views.detail_pesanan, name='detail-pesanan'),
    path('update/<str:id>/', views.update_pesanan, name='update-pesan'),
    path('delete/<str:id>/', views.delete_pesanan, name='delete-pesanan')
]