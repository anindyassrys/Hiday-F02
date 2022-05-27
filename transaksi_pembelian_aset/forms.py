from email.policy import default
from django import forms

class buat_aset_form(forms.Form):
    id = forms.CharField(label='ID', disabled=True)
    nama = forms.CharField(label='Nama', max_length=50)
    minimum_level = forms.CharField(label='Minimum Level', max_length=50)
    harga_beli = forms.CharField(label='Harga Beli', max_length=50)
    harga_jual = forms.CharField(label='Harga Jual', max_length=50)
    durasi_panen = forms.CharField(label='Durasi Panen', max_length=50)
    kapasitas_maks = forms.CharField(label='Kapasitas Maksimum', max_length=50)
    jenis_hewan = forms.CharField(label='Jenis Hewan', max_length=50)
    durasi_produksi = forms.CharField(label='Durasi Produksi', max_length=50)
    jenis_tanaman = forms.CharField(label='Jenis Tanaman', widget=forms.Select(choices=[]))