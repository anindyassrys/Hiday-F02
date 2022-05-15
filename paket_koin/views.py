from django.shortcuts import redirect, render
from django.db import connection

# Create your views here.
def create_paket_koin(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        role = request.session['email'][1]
        if role == "admin":
            if request.method == "POST":
                jumlah_koin = request.POST["jumlah_koin"]
                harga = request.POST["harga"]
                return redirect("paket_koin:list_paket")
            else:
                return render(request, ".html", {})
        else:
            return redirect("paket_koin:list_paket_koin")
    else:
        return redirect("home:login")

# Read paket_koin
def list_paket_koin(request):
    if request.session.has_key('email'):
        cursor = connection.cursor()

        if (request.session['email'][1] == "admin"):
            cursor.execute("SELECT * FROM paket_koin")
            result = cursor.fetchall()
            role = "admin"
        else:
            cursor.execute("SELECT * FROM paket_koin")
            result = cursor.fetchall()
            role = "pengguna"
        
    return render(request, 'list_paket_koin.html', {'results': result, 'role': role})


