from django.shortcuts import redirect, render
from django.db import connection

# Create paket
def create_paket_koin(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        role = request.session['email'][1]
        if role == "admin":
            if request.method == "POST":
                print("bryan gak ganteng")
                jumlah_koin = request.POST["jumlah_koin"]
                harga = request.POST["harga"]
                return redirect("paket_koin:list_paket")
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

        if (request.session['email'][1] == "admin"):
            cursor.execute("SELECT * FROM paket_koin")
            result = cursor.fetchall()
            role = "admin"
        else:
            cursor.execute("SELECT * FROM paket_koin")
            result = cursor.fetchall()
            role = "pengguna"
        
    return render(request, 'list_paket_koin.html', {'results': result, 'role': role})

#update paket_koin
def update_paket_koin(request, value, harga):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    
    if request.session.has_key('email'):
        role = request.session['email'][1]
        if role == "admin":
            if request.method == "POST":
                return redirect("paket_koin:list_paket")
            else:
                return render(request, 'ubah_paket_koin.html', {'value': value, 'role': role, 'harga':harga})
        else:
            return redirect("paket_koin:list_paket_koin")
    else:
        return redirect("home:login")


