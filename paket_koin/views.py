from django.shortcuts import redirect, render

# Create your views here.
def create_paket_koin(request):
    cursor = connection.cursor
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        role = request.session['role']
        if role == "admin":
            if request.method == "POST":
                jumlah_koin = request.POST["jumlah_koin"]
                harga = request.POST["harga"]
                return redirect("paket_koin:list_paket")
            else:
                return render(request, ".html", {})
        else:
            return redirect("paket_koin:list_paket")
    else:
        return redirect("home:login")

def list_paket(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('email'):
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None
    
    cursor.execute("SET search_path TO hidayf02")
    cursor.execute("SELECT * FROM paket_koin")
    data = cursor.fetchall()
    return render(request, '.html', {'data' : data, 'role' : role})

