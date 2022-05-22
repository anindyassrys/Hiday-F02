# from errno import EBADRQC
from gc import get_objects
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


def lihat_isi_lumbung(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        cursor.execute("SET search_path TO hidayf02")
        role = request.session['email'][1]
        email =request.session['email'][0]
        
 
        if role == 'admin': #lihat lumbung untuk admin
            # Produk Hasil Panen
            produk_hasil_panen = object_entitas('select email, id, nama, harga_jual, sifat_produk, jumlah from lumbung l, lumbung_memiliki_produk lmp, produk p where l.email = lmp.id_lumbung and lmp.id_produk = p.id and p.id in (select * from hasil_panen)')
            # Produk Hewan
            produk_hewan = object_entitas('select email, id, nama, harga_jual, sifat_produk, jumlah from lumbung l, lumbung_memiliki_produk lmp, produk p where l.email = lmp.id_lumbung and lmp.id_produk = p.id and p.id in (select * from produk_hewan)')
            # Produk Makanan
            produk_makanan = object_entitas('select email, id, nama, harga_jual, sifat_produk, jumlah from lumbung l, lumbung_memiliki_produk lmp, produk p where l.email = lmp.id_lumbung and lmp.id_produk = p.id and p.id in (select * from produk_makanan)')
            cursor.execute("SET search_path TO public")

            return render(request, 'lihat_isi_lumbung.html', {'role': role, 'produk_hasil_panen': produk_hasil_panen, 'produk_hewan': produk_hewan, 'produk_makanan': produk_makanan })
        else:               #lihat lumbung untuk pengguna (hanya punya dirinya sendiri)
            level_pengguna = request.session['email'][5]
            # print(request.session['email'])
            print("ga masuk")
            total_kapasitas_lumbung = 0

            level = request.session['email'][5]
            # Produk Hasil Panen
            x = cursor.execute('select email, id, nama, harga_jual, sifat_produk, jumlah from lumbung l, lumbung_memiliki_produk lmp, produk p where l.email = lmp.id_lumbung and lmp.id_produk = p.id and p.id in (select * from hasil_panen) and l.email = %s',[email])
            desc = cursor.description
            nt_result = namedtuple('Hasil_Panen', [col[0] for col in desc])
            result = [nt_result(*row) for row in cursor.fetchall()]

            number_result = {}
            # cursor.execute('SET search_path TO public')
            
            sum_of_entitites = range(len(result))
            for i in sum_of_entitites:
                number_result[i+1] = result[i]
            produk_hasil_panen = list(number_result.items())

            for j in result:
                total_kapasitas_lumbung = total_kapasitas_lumbung + j.jumlah
                # print(j.jumlah)
           
            # Produk Hewan
            # produk_hewan = object_entitas('select email, id, nama, harga_jual, sifat_produk, jumlah from lumbung l, lumbung_memiliki_produk lmp, produk p where l.email = lmp.id_lumbung and lmp.id_produk = p.id and p.id in (select * from produk_hewan) and l.email = %s',[email])
            y = cursor.execute('select email, id, nama, harga_jual, sifat_produk, jumlah from lumbung l, lumbung_memiliki_produk lmp, produk p where l.email = lmp.id_lumbung and lmp.id_produk = p.id and p.id in (select * from produk_hewan) and l.email = %s',[email])
            desc = cursor.description
            nt_result = namedtuple('Produk_Hewan', [col[0] for col in desc])
            result = [nt_result(*row) for row in cursor.fetchall()]

            number_result = {}
            # cursor.execute('SET search_path TO public')
            
            sum_of_entitites = range(len(result))
            for i in sum_of_entitites:
                number_result[i+1] = result[i]
            produk_hewan = list(number_result.items())

            for j in result:
                total_kapasitas_lumbung = total_kapasitas_lumbung + j.jumlah
            # Produk Makanan
            # produk_makanan = object_entitas('select email, id, nama, harga_jual, sifat_produk, jumlah from lumbung l, lumbung_memiliki_produk lmp, produk p where l.email = lmp.id_lumbung and lmp.id_produk = p.id and p.id in (select * from produk_makanan) and l.email = %s',[email])
            z = cursor.execute('select email, id, nama, harga_jual, sifat_produk, jumlah from lumbung l, lumbung_memiliki_produk lmp, produk p where l.email = lmp.id_lumbung and lmp.id_produk = p.id and p.id in (select * from produk_makanan) and l.email = %s',[email])
            desc = cursor.description
            nt_result = namedtuple('Produk_Hewan', [col[0] for col in desc])
            result = [nt_result(*row) for row in cursor.fetchall()]

            number_result = {}
            # cursor.execute('SET search_path TO public')
            
            sum_of_entitites = range(len(result))
            for i in sum_of_entitites:
                number_result[i+1] = result[i]
            produk_makanan = list(number_result.items())
            for j in result:
                total_kapasitas_lumbung = total_kapasitas_lumbung + j.jumlah
            print(total_kapasitas_lumbung)
            cursor.execute("SET search_path TO public")
            return render(request, 'lihat_isi_lumbung.html', {'role': role, 'produk_hasil_panen': produk_hasil_panen, 'produk_hewan': produk_hewan, 'produk_makanan': produk_makanan, 'level': level , 'total': total_kapasitas_lumbung})
    else:
        return redirect("home:login")

#list produk (pengguna dan admin)
def produk(request): 
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        cursor.execute("SET search_path TO hidayf02")
        role = request.session['email'][1]
        if role == 'admin':
            object_admin = object_entitas('SELECT id,nama,harga_jual,sifat_produk, CASE WHEN id LIKE ' + "'%hp%'" + ' THEN ' + "'Hasil Panen'" + 'WHEN id LIKE '+ "'%ph%'" + ' THEN ' + "'Produk Hewan'"  + 'WHEN id LIKE ' + "'%pm%'" + 'THEN ' + "'Produk Makanan'" + ' END AS jenis FROM PRODUK')
            cursor.execute("SET search_path TO public")
            # print(object_admin)
            return render(request, 'read_produk.html', {'results_admin': object_admin, 'role': role})
        else:
            # object_pengguna = object_entitas('SELECT * from PRODUK')
            object_pengguna = object_entitas('SELECT id,nama,harga_jual,sifat_produk, CASE WHEN id LIKE ' + "'%hp%'" + ' THEN ' + "'Hasil Panen'" + 'WHEN id LIKE '+ "'%ph%'" + ' THEN ' + "'Produk Hewan'"  + 'WHEN id LIKE ' + "'%pm%'" + 'THEN ' + "'Produk Makanan'" + ' END AS jenis FROM PRODUK')
            cursor.execute("SET search_path TO public")
            return render(request, 'read_produk.html', {'results_pengguna': object_pengguna, 'role': role})
    return redirect("home:login")

#buat/update produk (admin)

#list produksi (pengguna dan admin)
def produksi(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        role = request.session['email'][1]
        cursor.execute("SET search_path TO hidayf02")
        if role == 'admin':
            object_admin = object_entitas('SELECT p.nama, a.nama as nama_aset, pr.durasi, pr.jumlah_unit_hasil FROM PRODUK p, aset a, produksi pr WHERE p.id = pr.id_produk_makanan AND a.id = pr.id_alat_produksi')
            print(object_admin)
            cursor.execute("SET search_path TO public")
            return render(request, 'read_produksi.html', {'results_admin': object_admin, 'role': role})
        else:
            # object_pengguna = object_entitas('SELECT * from PRODUK')
            object_pengguna = object_entitas('SELECT p.nama, a.nama as nama_aset, pr.durasi, pr.jumlah_unit_hasil FROM PRODUK p, aset a, produksi pr WHERE p.id = pr.id_produk_makanan AND a.id = pr.id_alat_produksi')
            cursor.execute("SET search_path TO public")
            return render(request, 'read_produksi.html', {'results_pengguna': object_pengguna, 'role': role})
    return redirect("home:login")

#buat/update produksi(admin)

#list histori produk makanan (pengguna dan admin)
def histori_produk_makanan(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        role = request.session['email'][1]
        cursor.execute("SET search_path TO hidayf02")
        if role == 'admin':
            object_admin = object_entitas('SELECT hpm.email, hpm.waktu_awal, hp.waktu_selesai, hp.jumlah, hp.xp, p.nama , a.nama as nama_produk FROM histori_produksi hp, histori_produksi_makanan hpm, produk p, aset a WHERE hpm.waktu_awal = hp.waktu_awal AND hpm.id_alat_produksi = a.id AND hpm.id_produk_makanan = p.id')
            print(object_admin)
            cursor.execute("SET search_path TO public")
            return render(request, 'read_histori_produk_makanan.html', {'results_admin': object_admin, 'role': role})
        else:
            # object_pengguna = object_entitas('SELECT * from PRODUK')
            email = request.session['email'][0]
          
            # object_pengguna = object_entitas("SELECT hpm.email, hpm.waktu_awal, hp.waktu_selesai, hp.jumlah, hp.xp, p.nama, a.nama as nama_produk FROM histori_produksi hp, histori_produksi_makanan hpm, produk p, aset a WHERE hpm.waktu_awal = hp.waktu_awal AND hpm.id_alat_produksi = a.id AND hpm.id_produk_makanan = p.id AND hpm.email = %s",[email] )
            x = cursor.execute("SELECT hpm.email, hpm.waktu_awal, hp.waktu_selesai, hp.jumlah, hp.xp, p.nama, a.nama as nama_produk FROM histori_produksi hp, histori_produksi_makanan hpm, produk p, aset a WHERE hpm.waktu_awal = hp.waktu_awal AND hpm.id_alat_produksi = a.id AND hpm.id_produk_makanan = p.id AND hpm.email = %s",[email])
            desc = cursor.description
            nt_result = namedtuple('Hasil_Panen', [col[0] for col in desc])
            result = [nt_result(*row) for row in cursor.fetchall()]

            number_result = {}
            cursor.execute('SET search_path TO public')
            
            sum_of_entitites = range(len(result))
            for i in sum_of_entitites:
                number_result[i+1] = result[i]
            results_pengguna = list(number_result.items())
         
            cursor.execute("SET search_path TO public")
            return render(request, 'read_histori_produk_makanan.html', {'role': role, 'results_pengguna':results_pengguna })
    return redirect("home:login")

#create produk makanan (pengguna)

#details produksi
def produksi_details(request, slug):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO hidayf02")
    cursor.execute("SELECT p.nama, a.nama as nama_aset, pr.durasi, pr.jumlah_unit_hasil, p.id FROM PRODUK p, aset a, produksi pr WHERE p.id = pr.id_produk_makanan AND a.id = pr.id_alat_produksi and p.nama =  %s", [slug] )
    object_detail = cursor.fetchone()
   
    id_produk = object_detail[4]
    x = cursor.execute("select id_produk_makanan, p.nama as bahan, jumlah from produk_dibutuhkan_oleh_produk_makanan, produk p where id_produk = p.id AND id_produk_makanan = %s" ,[id_produk])
    desc = cursor.description
    nt_result = namedtuple('Hasil_Panen', [col[0] for col in desc])
    result = [nt_result(*row) for row in cursor.fetchall()]

    number_result = {}
    cursor.execute('SET search_path TO public')
    
    sum_of_entitites = range(len(result))
    for i in sum_of_entitites:
        number_result[i+1] = result[i]
    x = list(number_result.items())
    context = {
        'nama_produk' : object_detail[0],
        'alat_produski' :object_detail[1],
        'durasi' : object_detail[2],
        'jumlah' : object_detail[3],
    }

    cursor.execute('SET search_path TO public')
    return render(request, 'details_produksi.html', {'object' : context, 'object_bahan':x } )
  


def object_entitas(query): # mengembalikan value relasi dalam bentuk object (class) dalam bentuk list
     # source code: https://dev.to/stndaru/connecting-django-to-postgresql-on-heroku-and-perform-sql-command-4m8e
    cursor = connection.cursor()
    cursor.execute("SET search_path TO hidayf02")
    result = []
    cursor.execute(query)

    desc = cursor.description
    nt_result = namedtuple('Hasil_Panen', [col[0] for col in desc])
    
    result = [nt_result(*row) for row in cursor.fetchall()]

    # print('2')
    number_result = {}
    cursor.execute('SET search_path TO public')

    # sum_of_entitites = range(len(result)-1)
    sum_of_entitites = range(len(result))
    for i in sum_of_entitites:
        number_result[i+1] = result[i]
    
    return list(number_result.items())

def create_produk(request): # membuat produk (admin)
    return render(request, 'create_produk.html')


def update_produk(request): # membuat produk (admin)
    return render(request, 'update_produk.html')


def create_histori_produk_makanan(request): # membuat produk (admin)
    return render(request, 'create_histori_produk_makanan.html')

def register_admin(request): # membuat produk (admin)
    return render(request, 'registrasi_admin.html')

def register_pengguna(request): # membuat produk (admin)
    return render(request, 'registriasi_pengguna.html')