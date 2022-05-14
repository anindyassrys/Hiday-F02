import imp
from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(label='E-Mail', max_length= 30)
    password = forms.CharField(label='Password', max_length=30)


class RegistrasiAdmin(forms.Form):
    email = forms.CharField(label="E-mail", max_length=30)
    password = forms.CharField(label="Password", max_length=30)

class RegistrasiPengguna(forms.Form):
    email = forms.CharField(label="E-mail", max_length=30)
    password = forms.CharField(label="Password", max_length=30)
    nama_area_pertanian = forms.CharField(label = "Nama-Area", max_length= 30)