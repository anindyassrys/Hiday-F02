from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render


def home(request):
    return render(request, 'home.html')

def login(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if not request.session.has_key('email'):
        cursor.execute("SET search_path TO hidayf02")
        if request.method == "POST":
            email = request.POST["email"]
            password = request.POST["password"]
            cursor.execute("SELECT email FROM akun WHERE email = %s", [email])
            target = cursor.fetchone()

            if target is not None:
                cursor.execute("SELECT email FROM admin WHERE email = %s", [email])
                admin_check = cursor.fetchone()

                cursor.execute("SELECT email FROM pengguna WHERE email = %s", [email])
                pengguna_check = cursor.fetchone()

                if admin_check is not None:
                    role = "admin"
                    cursor.execute("SELECT email, password FROM admin WHERE email = %s AND password = %s", [email, password])
                else:
                    role = "pengguna"
                    cursor.execute("SELECT email, password FROM pengguna WHERE email = %s AND password = %s", [email, password])
                
                if cursor.fetchone() is not None:
                    cursor.execute("SET search_path TO public")
                    request.session['email'] = email
                    request.session['role'] = role
                    return HttpResponseRedirect("/main")
                
            cursor.execute("SET search_path TO public")
            return redirect("home:login")
        
        else:
            cursor.execute("SET search_path TO public")
            return render(request, "login.html", {})
    else:
        return redirect("home:main")

def main(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        role = request.session['role']
        return render(request, 'main.html', {'role': role})
    else:
        return redirect("home:login")

def logout(request):
    try:
        del request.session['email']
        del request.session['role']
    except:
        pass
    return HttpResponseRedirect("/")



        
        


