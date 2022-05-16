from django.shortcuts import redirect, render
from django.db import connection

def produksi_tanaman(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        role = request.session['email'][1]
        if role == "pengguna":
            if request.method == "POST":
                return redirect("histori_tanaman:list_histori_tanaman")
            else:
                return render(request, 'produksi_tanaman.html', {})
        else:
            return redirect("histori_tanaman:list_histori_tanaman")
    else:
        return redirect("home:login")

def list_histori_tanaman(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        cursor.execute("SET search_path TO hidayf02")

        if (request.session['email'][1] == "admin"):
            cursor.execute("select hp.email, hp.waktu_awal, hp.waktu_selesai, hp.jumlah, hp.xp, a.nama from histori_produksi hp JOIN histori_tanaman ht on hp.email = ht.email and hp.waktu_awal = ht.waktu_awal JOIN bibit_tanaman bt on ht.id_bibit_tanaman = bt.id_aset JOIN aset a on bt.id_aset = a.id;")
            result = cursor.fetchall()
            role = "admin"
        else:
            cursor.execute("select hp.email, hp.waktu_awal, hp.waktu_selesai, hp.jumlah, hp.xp, a.nama from histori_produksi hp JOIN histori_tanaman ht on hp.email = ht.email and hp.waktu_awal = ht.waktu_awal JOIN bibit_tanaman bt on ht.id_bibit_tanaman = bt.id_aset JOIN aset a on bt.id_aset = a.id WHERE hp.email = '" + request.session['email'][1] + "'")
            result = cursor.fetchall()
            role = "pengguna"
        
    return render(request, 'list_produksi_tanaman.html', {'results': result, 'role': role})
