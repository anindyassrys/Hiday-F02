from django import forms
from django.db import connection

def inc(code, inc_id):
        res = code
        nilai = int(inc_id)
        nilai += 1
        res += str(nilai).zfill(3)
        return res

class form_buat_dekorasi(forms.Form):
    id_aset = forms.CharField(label=("ID Aset"), required=True, max_length=5)
    nama = forms.CharField(label=("Nama"), required=True, max_length=50)
    minimum_level = forms.IntegerField(label=("Minimum Level"), required=True)
    harga_beli = forms.IntegerField(label=("Harga Beli"), required=True)
    harga_jual = forms.IntegerField(label=("Harga Jual"), required=True)

    def __init__(self, *args, **kwargs):
        super(form_buat_dekorasi, self).__init__(*args, **kwargs)
        self.fields['id_aset'].widget.attrs['readonly'] = True
        self.fields['id_aset'].widget.attrs['class'] = 'disabled'

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT ID FROM hidayf02.ASET WHERE ID LIKE 'DK%' ORDER BY ID DESC LIMIT 1")
            new_id = inc("DK",cursor.fetchall()[0][0][2:])
        self.fields['id_aset'].initial = new_id

class form_update_dekorasi(forms.Form):
    id_aset = forms.CharField(label=("ID Aset"), required=True, max_length=5)
    nama = forms.CharField(label=("Nama"), required=True, max_length=50)
    minimum_level = forms.IntegerField(label=("Minimum Level"), required=True)
    harga_beli = forms.IntegerField(label=("Harga Beli"), required=True)
    harga_jual = forms.IntegerField(label=("Harga Jual"), required=True)

    def __init__(self, *args, **kwargs):
        super(form_update_dekorasi, self).__init__(*args, **kwargs)
        self.fields['id_aset'].widget.attrs['readonly'] = True
        self.fields['id_aset'].widget.attrs['class'] = 'disabled'
        self.fields['nama'].widget.attrs['readonly'] = True
        self.fields['nama'].widget.attrs['class'] = 'disabled'

class form_buat_bibit_tanaman(forms.Form):
    id_aset = forms.CharField(label=("ID Aset"), required=True, max_length=5)
    nama = forms.CharField(label=("Nama"), required=True, max_length=50)
    minimum_level = forms.IntegerField(label=("Minimum Level"), required=True)
    harga_beli = forms.IntegerField(label=("Harga Beli"), required=True)
    durasi_panen = forms.TimeField(label=("Durasi Panen"), required=True)

    def __init__(self, *args, **kwargs):
        super(form_buat_bibit_tanaman, self).__init__(*args, **kwargs)
        self.fields['id_aset'].widget.attrs['readonly'] = True
        self.fields['id_aset'].widget.attrs['class'] = 'disabled'

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT ID FROM hidayf02.ASET WHERE ID LIKE 'BT%' ORDER BY ID DESC LIMIT 1")
            new_id = inc("BT",cursor.fetchall()[0][0][2:])
        self.fields['id_aset'].initial = new_id

class form_update_bibit_tanaman(forms.Form):
    id_aset = forms.CharField(label=("ID Aset"), required=True, max_length=5)
    nama = forms.CharField(label=("Nama"), required=True, max_length=50)
    minimum_level = forms.IntegerField(label=("Minimum Level"), required=True)
    harga_beli = forms.IntegerField(label=("Harga Beli"), required=True)
    durasi_panen = forms.TimeField(label=("Durasi Panen"), required=True)

    def __init__(self, *args, **kwargs):
        super(form_update_bibit_tanaman, self).__init__(*args, **kwargs)
        self.fields['id_aset'].widget.attrs['readonly'] = True
        self.fields['id_aset'].widget.attrs['class'] = 'disabled'
        self.fields['nama'].widget.attrs['readonly'] = True
        self.fields['nama'].widget.attrs['class'] = 'disabled'

class form_buat_kandang(forms.Form):
    daftar_hewan = []
    id_aset = forms.CharField(label=("ID Aset"), required=True, max_length=5)
    nama = forms.CharField(label=("Nama"), required=True, max_length=50)
    minimum_level = forms.IntegerField(label=("Minimum Level"), required=True)
    harga_beli = forms.IntegerField(label=("Harga Beli"), required=True)
    kapasitas_maks = forms.IntegerField(label=("Kapasitas Maks"), required=True)
    jenis_hewan = forms.CharField(label=("Jenis Hewan"), required=True)

    def __init__(self, *args, **kwargs):
        super(form_buat_kandang, self).__init__(*args, **kwargs)
        self.fields['id_aset'].widget.attrs['readonly'] = True
        self.fields['id_aset'].widget.attrs['class'] = 'disabled'

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT ID FROM hidayf02.ASET WHERE ID LIKE 'KD%' ORDER BY ID DESC LIMIT 1")
            new_id = inc("KD",cursor.fetchall()[0][0][2:])
            self.fields['id_aset'].initial = new_id

class form_update_kandang(forms.Form):
    id_aset = forms.CharField(label=("ID Aset"), required=True, max_length=5)
    nama = forms.CharField(label=("Nama"), required=True, max_length=50)
    minimum_level = forms.IntegerField(label=("Minimum Level"), required=True)
    harga_beli = forms.IntegerField(label=("Harga Beli"), required=True)
    kapasitas_maks = forms.IntegerField(label=("Kapasitas Maks"), required=True)
    jenis_hewan = forms.CharField(label=("Jenis Hewan"), required=True)

    def __init__(self, *args, **kwargs):
        super(form_update_kandang, self).__init__(*args, **kwargs)
        self.fields['id_aset'].widget.attrs['readonly'] = True
        self.fields['id_aset'].widget.attrs['class'] = 'disabled'
        self.fields['nama'].widget.attrs['readonly'] = True
        self.fields['nama'].widget.attrs['class'] = 'disabled'
        self.fields['jenis_hewan'].widget.attrs['readonly'] = True
        self.fields['jenis_hewan'].widget.attrs['class'] = 'disabled'

class form_buat_hewan(forms.Form):
    id_aset = forms.CharField(label=("ID Aset"), required=True, max_length=5)
    nama = forms.CharField(label=("Nama"), required=True, max_length=50)
    minimum_level = forms.IntegerField(label=("Minimum Level"), required=True)
    harga_beli = forms.IntegerField(label=("Harga Beli"), required=True)
    durasi_produksi = forms.TimeField(label=("Durasi Produksi"), required=True)

    def __init__(self, *args, **kwargs):
        super(form_buat_hewan, self).__init__(*args, **kwargs)
        self.fields['id_aset'].widget.attrs['readonly'] = True
        self.fields['id_aset'].widget.attrs['class'] = 'disabled'

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT ID FROM hidayf02.ASET WHERE ID LIKE 'HW%' ORDER BY ID DESC LIMIT 1")
            new_id = inc("HW",cursor.fetchall()[0][0][2:])
        self.fields['id_aset'].initial = new_id

class form_update_hewan(forms.Form):
    id_aset = forms.CharField(label=("ID Aset"), required=True, max_length=5)
    nama = forms.CharField(label=("Nama"), required=True, max_length=50)
    minimum_level = forms.IntegerField(label=("Minimum Level"), required=True)
    harga_beli = forms.IntegerField(label=("Harga Beli"), required=True)
    durasi_produksi = forms.TimeField(label=("Durasi Produksi"), required=True)
    id_kandang = forms.CharField(label=("ID Kandang"), required=True)

    def __init__(self, *args, **kwargs):
        super(form_update_hewan, self).__init__(*args, **kwargs)
        self.fields['id_aset'].widget.attrs['readonly'] = True
        self.fields['id_aset'].widget.attrs['class'] = 'disabled'
        self.fields['nama'].widget.attrs['readonly'] = True
        self.fields['nama'].widget.attrs['class'] = 'disabled'
        self.fields['id_kandang'].widget.attrs['readonly'] = True
        self.fields['id_kandang'].widget.attrs['class'] = 'disabled'

class form_buat_alat_produksi(forms.Form):
    id_aset = forms.CharField(label=("ID Aset"), required=True, max_length=5)
    nama = forms.CharField(label=("Nama"), required=True, max_length=50)
    minimum_level = forms.IntegerField(label=("Minimum Level"), required=True)
    harga_beli = forms.IntegerField(label=("Harga Beli"), required=True)
    kapasitas_maks = forms.CharField(label=("Kapasitas Maksimum"), required=True)

    def __init__(self, *args, **kwargs):
        super(form_buat_alat_produksi, self).__init__(*args, **kwargs)
        self.fields['id_aset'].widget.attrs['readonly'] = True
        self.fields['id_aset'].widget.attrs['class'] = 'disabled'

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT ID FROM hidayf02.ASET WHERE ID LIKE 'AP%' ORDER BY ID DESC LIMIT 1")
            new_id = inc("AP",cursor.fetchall()[0][0][2:])
        self.fields['id_aset'].initial = new_id

class form_update_alat_produksi(forms.Form):
    id_aset = forms.CharField(label=("ID Aset"), required=True, max_length=5)
    nama = forms.CharField(label=("Nama"), required=True, max_length=50)
    minimum_level = forms.IntegerField(label=("Minimum Level"), required=True)
    harga_beli = forms.IntegerField(label=("Harga Beli"), required=True)
    kapasitas_maks = forms.CharField(label=("Kapasitas Maksimum"), required=True)

    def __init__(self, *args, **kwargs):
        super(form_update_alat_produksi, self).__init__(*args, **kwargs)
        self.fields['id_aset'].widget.attrs['readonly'] = True
        self.fields['id_aset'].widget.attrs['class'] = 'disabled'
        self.fields['nama'].widget.attrs['readonly'] = True
        self.fields['nama'].widget.attrs['class'] = 'disabled'

class form_buat_petak_sawah(forms.Form):
    list_tanaman = []
    id_aset = forms.CharField(label=("ID Aset"), required=True, max_length=5)
    nama = forms.CharField(label=("Nama"), required=True, max_length=50)
    minimum_level = forms.IntegerField(label=("Minimum Level"), required=True)
    harga_beli = forms.IntegerField(label=("Harga Beli"), required=True)
    jenis_tanaman = forms.ChoiceField(label=("Jenis Tanaman"), choices=list_tanaman, required=True)

    def __init__(self, *args, **kwargs):
        super(form_buat_petak_sawah, self).__init__(*args, **kwargs)
        self.fields['id_aset'].widget.attrs['readonly'] = True
        self.fields['id_aset'].widget.attrs['class'] = 'disabled'

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT ID FROM hidayf02.ASET WHERE ID LIKE 'PS%' ORDER BY ID DESC LIMIT 1")
            new_id = inc("PS",cursor.fetchall()[0][0][2:])
            cursor.execute(
                "SELECT nama,nama FROM hidayf02.ASET, hidayf02.BIBIT_TANAMAN WHERE ID=ID_ASET ORDER BY ID ASC")
            self.fields['jenis_tanaman'].choices = cursor.fetchall()

        self.fields['id_aset'].initial = new_id

class form_update_petak_sawah(forms.Form):
    list_tanaman = []
    id_aset = forms.CharField(label=("ID Aset"), required=True, max_length=5)
    nama = forms.CharField(label=("Nama"), required=True, max_length=50)
    minimum_level = forms.IntegerField(label=("Minimum Level"), required=True)
    harga_beli = forms.IntegerField(label=("Harga Beli"), required=True)
    jenis_tanaman = forms.ChoiceField(label=("Jenis Tanaman"), choices=list_tanaman, required=True)

    def __init__(self, *args, **kwargs):
        super(form_update_petak_sawah, self).__init__(*args, **kwargs)
        self.fields['id_aset'].widget.attrs['readonly'] = True
        self.fields['id_aset'].widget.attrs['class'] = 'disabled'
        self.fields['nama'].widget.attrs['readonly'] = True
        self.fields['nama'].widget.attrs['class'] = 'disabled'

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT nama,nama FROM hidayf02.ASET, hidayf02.BIBIT_TANAMAN WHERE ID=ID_ASET ORDER BY ID ASC")
            self.fields['jenis_tanaman'].choices = cursor.fetchall()

