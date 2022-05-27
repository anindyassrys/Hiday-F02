from sqlite3 import Cursor
from unittest import result
from django.shortcuts import redirect, render
from django.db import connection

# Create paket koin
def create_paket_koin(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        role = request.session['email'][1]
        if role == "admin":
            if request.method == "POST":
                jumlah_koin = request.POST["jumlah_koin"]
                harga = request.POST["harga"]
                cursor.execute("SET search_path to hidayf02")
                cursor.execute("""INSERT INTO paket_koin (jumlah_koin, harga) VALUES ('"""+jumlah_koin+"""', '"""+harga+"""')""")
                return redirect("paket_koin:list_paket_koin")
            else:
                return render(request, "create_paket_koin.html", {})
        else:
            return redirect("paket_koin:list_paket_koin")
    else:
        return redirect("home:login")

# Read paket_koin
def list_paket_koin(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        cursor.execute("SET search_path TO hidayf02")
        cursor.execute("SELECT paket_koin, total_biaya FROM transaksi_pembelian_koin")
        deleteable = cursor.fetchall()

        if (request.session['email'][1] == "admin"):
            cursor.execute("SELECT * FROM paket_koin")
            result = cursor.fetchall()
            role = "admin"

            if request.method == "POST":
                jumlah_koin = request.POST["jumlah_koin"]
                harga = request.POST["harga"]
                cursor.execute("DELETE FROM paket_koin WHERE jumlah_koin = %s and harga = %s", [jumlah_koin, harga])
                return redirect("paket_koin:list_paket_koin")

        else:
            cursor.execute("SELECT * FROM paket_koin")
            result = cursor.fetchall()
            role = "pengguna"
        
    return render(request, 'list_paket_koin.html', {'results': result, 'role': role, 'deleteable': deleteable})

#update paket_koin
def update_paket_koin(request, jumlah_koin, harga):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    
    if request.session.has_key('email'):
        role = request.session['email'][1]
        if role == "admin":
            if request.method == "POST":
                harga = request.POST["harga"]
                cursor.execute("SET search_path to hidayf02")
                cursor.execute("UPDATE paket_koin SET harga = %s where jumlah_koin = %s", [harga, jumlah_koin])
                return redirect("paket_koin:list_paket_koin")
            else:
                return render(request, 'ubah_paket_koin.html', {'value': jumlah_koin, 'role': role, 'harga':harga})
        else:
            return redirect("paket_koin:list_paket_koin")
    else:
        return redirect("home:login")

#create transaksi_pembelian_koin
def create_transaksi_pembelian_paket_koin(request, value, harga):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    
    if request.session.has_key('email'):
        role = request.session['email'][1]
        cara_pembayaran = ""
        jumlah = 0
        total_biaya = 0

        if role == "pengguna":
            if request.method == "POST":
                cara_pembayaran = request.POST["cara_pembayaran"]
                jumlah = int(request.POST["jumlah"])
                total_biaya = jumlah*int(harga)

                cursor.execute("SET search_path to hidayf02")
                cursor.execute("SELECT (NOW() + interval '7 hours')::timestamp")
                result_time = cursor.fetchall()
                time = str(result_time[0][0])

                cursor.execute("INSERT INTO transaksi_pembelian_koin VALUES ('"+request.session['email'][0]+"', '"+ time + "'::timestamp, '"+ str(jumlah)+"', '"+str(cara_pembayaran)+"', '"+str(value)+"', '"+ str(total_biaya)+"')")
                return redirect("paket_koin:list_transaksi_pembelian_koin")
            else:
                return render(request, 'create_transaksi_pembelian_koin.html', {'value': value, 'role': role, 'harga':harga, 'cara_pembayaran':cara_pembayaran, 'jumlah':jumlah})
        else:
            return redirect("paket_koin:list_transaksi_pembelian_koin")
    else:
        return redirect("home:login")
        
#read transaksi_pembelian_koin
def list_transaksi_pembelian_koin(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        cursor.execute("SET search_path TO hidayf02")

        if (request.session['email'][1] == "admin"):
            cursor.execute("SELECT * FROM transaksi_pembelian_koin")
            result = cursor.fetchall()
            role = "admin"
        else:
            cursor.execute("SELECT * FROM transaksi_pembelian_koin WHERE email = '" + request.session['email'][0] + "' ")
            result = cursor.fetchall()
            role = "pengguna"
    return render(request, 'list_transaksi_pembelian_koin.html', {'results': result, 'role': role})