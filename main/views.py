from pickle import NONE
from re import X
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import redirect, render
from collections import namedtuple
from django.contrib import messages
from .form import *

def login(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if not request.session.has_key('email'):
        cursor.execute("SET search_path TO hidayf02")
        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['password']

            cursor.execute("SELECT email FROM akun WHERE email = %s", [email])
            target = cursor.fetchone()

            if target is not None: #mengecek apakah user tersebut tedapat pada database
                cursor.execute("SELECT email, password FROM admin WHERE email = %s AND password = %s", [email, password])
                admin_check = cursor.fetchone()

                cursor.execute("SELECT * FROM pengguna WHERE email = %s AND password = %s", [email, password])
                pengguna_check = cursor.fetchone()

                if admin_check is not None: #jika admin
                    role = "admin"
                    request.session['email'] = [email, role]
                    cursor.execute("SET search_path TO public")
                    return HttpResponseRedirect("/home")

                if pengguna_check is not None:      #jika pengguna
                    role = "pengguna"  
                    area_pertanian = pengguna_check[2]
                    xp_pengguna = pengguna_check[3]
                    koin_pengguna = pengguna_check[4]
                    level_pengguna = pengguna_check[5]
                    request.session['email'] = [email,role, area_pertanian, xp_pengguna,koin_pengguna,level_pengguna]
                    cursor.execute("SET search_path TO public")
                    return HttpResponseRedirect("/home")

                return HttpResponseNotFound("The user does not exist")
            
            cursor.execute("SET search_path TO public")
            return redirect("home:login")

        else:
            cursor.execute("SET search_path TO public")
            return render(request, "login.html", {})
            # return HttpResponseNotFound("The user does not exist")
    else:
        return redirect("home:home")

def home(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        role = request.session['email'][1]
        # print(role)
        if role == 'admin': #homepage untuk admin
            email_admin = request.session['email'][0]
            return render(request, 'home.html', {'role': role, 'email' : email_admin})
        else:               #homepage untuk pengguna
            area_pertanian = request.session['email'][2]
            xp_pengguna = request.session['email'][3]
            koin_pengguna = request.session['email'][4]
            level_pengguna = request.session['email'][5]
            return render(request, 'home.html', {'role': role, 'area': area_pertanian, 'xp':xp_pengguna, 'koin' : koin_pengguna, 'level' :level_pengguna})
    else:
        return redirect("home:login")

def logout(request):
    try:
        del request.session['email']
        # del request.session['role']
    except:
        pass
    return HttpResponseRedirect("/")

def produk(request): 
    cursor = connection.cursor()
    cursor.execute("SET search_path TO hidayf02")


    # source code: https://dev.to/stndaru/connecting-django-to-postgresql-on-heroku-and-perform-sql-command-4m8e
    
    x = object_entitas('SELECT * from PRODUK')
    cursor.execute("SET search_path TO public")
    return render(request, 'produk_list.html', {'results': x})

def lihat_isi_lumbung(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        cursor.execute("SET search_path TO hidayf02")
        role = request.session['email'][1]
       
        # Produk Hasil Panen
        produk_hasil_panen = object_entitas('select email, id, nama, harga_jual, sifat_produk, jumlah from lumbung l, lumbung_memiliki_produk lmp, produk p where l.email = lmp.id_lumbung and lmp.id_produk = p.id and p.id in (select * from hasil_panen)')
        # Produk Hewan
        produk_hewan = object_entitas('select email, id, nama, harga_jual, sifat_produk, jumlah from lumbung l, lumbung_memiliki_produk lmp, produk p where l.email = lmp.id_lumbung and lmp.id_produk = p.id and p.id in (select * from produk_hewan)')
        # Produk Makanan
        produk_makanan = object_entitas('select email, id, nama, harga_jual, sifat_produk, jumlah from lumbung l, lumbung_memiliki_produk lmp, produk p where l.email = lmp.id_lumbung and lmp.id_produk = p.id and p.id in (select * from produk_makanan)')
 
        if role == 'admin': #homepage untuk admin
            cursor.execute("SET search_path TO public")
            return render(request, 'lihat_isi_lumbung.html', {'role': role, 'produk_hasil_panen': produk_hasil_panen, 'produk_hewan': produk_hewan, 'produk_makanan': produk_makanan })
        else:               #homepage untuk pengguna
            level_pengguna = request.session['email'][5]
            cursor.execute("SET search_path TO public")
            return render(request, 'lihat_isi_lumbung.html', {'role': role, 'produk_hasil_panen': produk_hasil_panen, 'produk_hewan': produk_hewan, 'produk_makanan': produk_makanan })
    else:
        return redirect("home:login")

def object_entitas(query): # mengembalikan value relasi dalam bentuk object (class) dalam bentuk list
     # source code: https://dev.to/stndaru/connecting-django-to-postgresql-on-heroku-and-perform-sql-command-4m8e
    cursor = connection.cursor()
    cursor.execute("SET search_path TO hidayf02")
    result = []
    cursor.execute(query)

    desc = cursor.description
    nt_result = namedtuple('Hasil_Panen', [col[0] for col in desc])
    result = [nt_result(*row) for row in cursor.fetchall()]
    number_result = {}
    cursor.execute('SET search_path TO public')

    sum_of_entitites = range(len(result)-1)
    for i in sum_of_entitites:
        number_result[i+1] = result[i]
    
    return list(number_result.items())
