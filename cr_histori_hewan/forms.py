from email.policy import default
from django import forms

class produksi_hewan_form(forms.Form):
    id_hewan = forms.CharField(label='IdHewan', widget=forms.Select(choices=[]))
    jumlah = forms.CharField(label='Jumlah')
    XP = forms.IntegerField(label='XP', initial=5, disabled=True)
