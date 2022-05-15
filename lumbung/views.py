from django.shortcuts import redirect, render
from django.db import connection

#create transaksi_pembelian_koin
def upgrade_lumbung(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        role = request.session['email'][1]
        if role == "pengguna":
            if request.method == "POST":
                return redirect("lumbung:list_transaksi_upgrade_lumbung")
            else:
                return render(request, 'upgrade_lumbung.html', {})
        else:
            return redirect("lumbung:list_transaksi_upgrade_lumbung")
    else:
        return redirect("home:login")

#read upgrade lumbung
def list_transaksi_upgrade_lumbung(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        cursor.execute("SET search_path TO hidayf02")

        if (request.session['email'][1] == "admin"):
            cursor.execute("SELECT * FROM transaksi_upgrade_lumbung")
            result = cursor.fetchall()
            role = "admin"
        else:
            cursor.execute("SELECT * FROM transaksi_upgrade_lumbung WHERE email = '" + request.session['email'][1] + "'")
            result = cursor.fetchall()
            role = "pengguna"
        
    return render(request, 'list_transaksi_upgrade_lumbung.html', {'results': result, 'role': role})
