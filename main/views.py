from cmath import pi

from doctest import FAIL_FAST, master
from gc import get_objects
from pickle import FALSE, NONE, TRUE

from re import X
from datetime import datetime
from tokenize import Name
from traceback import print_tb
from turtle import update
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
            email_pengguna = request.session['email'][0]
            area_pertanian = request.session['email'][2]
            xp_pengguna = request.session['email'][3]
            koin_pengguna = request.session['email'][4]
            level_pengguna = request.session['email'][5]
            return render(request, 'home.html', {'role': role, 'area': area_pertanian, 'xp':xp_pengguna, 'koin' : koin_pengguna, 'level' :level_pengguna, 'email': email_pengguna})
    else:
        return redirect("home:login")

def logout(request):
    try:
        print(request.session['email'])
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
            kumpulan_id = []
            cursor.execute("SET search_path TO hidayf02")
            cursor.execute('select id_produk from detail_pesanan')
            for i in cursor.fetchall():
                kumpulan_id.append(i[0])

            cursor.execute('select id_produk from lumbung_memiliki_produk')
            for i in cursor.fetchall():
                kumpulan_id.append(i[0])

            cursor.execute('select id_produk_makanan from produk_dibutuhkan_oleh_produk_makanan')
            for i in cursor.fetchall():
                kumpulan_id.append(i[0])

            cursor.execute('select id_produk from produk_dibutuhkan_oleh_produk_makanan')
            for i in cursor.fetchall():
                kumpulan_id.append(i[0])

            cursor.execute('select id_produk_makanan from produksi')
            for i in cursor.fetchall():
                kumpulan_id.append(i[0])

            cursor.execute('select id_produk_hewan from hewan_menghasilkan_produk_hewan')
            for i in cursor.fetchall():
                kumpulan_id.append(i[0])

            cursor.execute('select id_hasil_panen from bibit_tanaman_menghasilkan_hasil_panen')
            for i in cursor.fetchall():
                kumpulan_id.append(i[0])
    
            cursor.execute('SELECT id,nama,harga_jual,sifat_produk, CASE WHEN id LIKE ' + "'%hp%'" + ' THEN ' + "'Hasil Panen'" + 'WHEN id LIKE '+ "'%ph%'" + ' THEN ' + "'Produk Hewan'"  + 'WHEN id LIKE ' + "'%pm%'" + 'THEN ' + "'Produk Makanan'" + ' END AS jenis FROM PRODUK')
            desc = cursor.description
            nt_result = []
            for col in desc:
                nt_result.append(col[0])
            
            nt_result.append('bisa_didelete')
         
            object_admin = namedtuple('object_produk_admin',nt_result)

            result = []
            for row in cursor.fetchall():
                if row[0] in kumpulan_id:
                    result.append(object_admin(row[0],row[1],row[2],row[3],row[4],'kadit_sabi'))
                else:
                    result.append(object_admin(row[0],row[1],row[2],row[3],row[4],'sabiyuawal_sabiyulakhir'))
            # print(result)
            number_result = {}
            

            # sum_of_entitites = range(len(result)-1)
            sum_of_entitites = range(len(result))
            for i in sum_of_entitites:
                number_result[i+1] = result[i]
            
            x = list(number_result.items())
            # print(x)
            cursor.execute("SET search_path TO public")
            return render(request, 'read_produk.html', {'results_admin': x, 'role': role})
        else:
            # object_pengguna = object_entitas('SELECT * from PRODUK')
            object_pengguna = object_entitas('SELECT id,nama,harga_jual,sifat_produk, CASE WHEN id LIKE ' + "'%hp%'" + ' THEN ' + "'Hasil Panen'" + 'WHEN id LIKE '+ "'%ph%'" + ' THEN ' + "'Produk Hewan'"  + 'WHEN id LIKE ' + "'%pm%'" + 'THEN ' + "'Produk Makanan'" + ' END AS jenis FROM PRODUK')
            cursor.execute("SET search_path TO public")
            return render(request, 'read_produk.html', {'results_pengguna': object_pengguna, 'role': role})
    return redirect("home:login")

#list produksi (pengguna dan admin)
def produksi(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        role = request.session['email'][1]
        cursor.execute("SET search_path TO hidayf02")
        if role == 'admin':

            ################################
            kumpulan_id = []
            cursor.execute('select id_alat_produksi ,id_produk_makanan from histori_produksi_makanan')
            for i in cursor.fetchall():
                kumpulan_id.append([i[0], i[1]])

     

            cursor.execute('SELECT p.id, a.id id_aset, p.nama, a.nama as nama_aset, pr.durasi, pr.jumlah_unit_hasil FROM PRODUK p, aset a, produksi pr WHERE p.id = pr.id_produk_makanan AND a.id = pr.id_alat_produksi')
            desc = cursor.description
            nt_result = []
            for col in desc:
                nt_result.append(col[0])
            
            nt_result.append('bisa_didelete')
         
            object_admin = namedtuple('object_produk_admin',nt_result)
            keadilan = False
            result = []
            for row in cursor.fetchall():
                for i in kumpulan_id:
                    if([row[1],row[0]] == i):
                        keadilan = True
                if(keadilan): 
                    result.append(object_admin(row[0],row[1],row[2],row[3],row[4],row[5],'kadit_sabi'))
                    keadilan = False
                else:
                    result.append(object_admin(row[0],row[1],row[2],row[3],row[4],row[5],'sabiyuawal_sabiyulakhir'))
            number_result = {}
            
            sum_of_entitites = range(len(result))
            for i in sum_of_entitites:
                number_result[i+1] = result[i]
            
            x = list(number_result.items())
            ###################################

            cursor.execute("SET search_path TO public")
            return render(request, 'read_produksi.html', {'results_admin': x, 'role': role})
        else:
            # object_pengguna = object_entitas('SELECT * from PRODUK')
            object_pengguna = object_entitas('SELECT p.id, p.nama, a.nama as nama_aset, pr.durasi, pr.jumlah_unit_hasil FROM PRODUK p, aset a, produksi pr WHERE p.id = pr.id_produk_makanan AND a.id = pr.id_alat_produksi')
            cursor.execute("SET search_path TO public")
            return render(request, 'read_produksi.html', {'results_pengguna': object_pengguna, 'role': role})
    return redirect("home:login")

#list histori produk makanan (pengguna dan admin)
def histori_produk_makanan(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        role = request.session['email'][1]
        cursor.execute("SET search_path TO hidayf02")
        if role == 'admin':
            object_admin = object_entitas('SELECT hpm.email, hpm.waktu_awal, hp.waktu_selesai, hp.jumlah, hp.xp, p.nama , a.nama as nama_produk FROM histori_produksi hp, histori_produksi_makanan hpm, produk p, aset a WHERE hpm.waktu_awal = hp.waktu_awal AND hpm.id_alat_produksi = a.id AND hpm.id_produk_makanan = p.id')
            # print(object_admin)
            cursor.execute("SET search_path TO public")
            return render(request, 'read_histori_produk_makanan.html', {'results_admin': object_admin, 'role': role})
        else:
            # object_pengguna = object_entitas('SELECT * from PRODUK')
            email = request.session['email'][0]
          
            # object_pengguna = object_entitas("SELECT hpm.email, hpm.waktu_awal, hp.waktu_selesai, hp.jumlah, hp.xp, p.nama, a.nama as nama_produk FROM histori_produksi hp, histori_produksi_makanan hpm, produk p, aset a WHERE hpm.waktu_awal = hp.waktu_awal AND hpm.id_alat_produksi = a.id AND hpm.id_produk_makanan = p.id AND hpm.email = %s",[email] )
            x = cursor.execute("select hp.waktu_awal, hp.waktu_selesai, jumlah, xp, p.nama as produk_makanan, a.nama as aset from histori_produksi hp, histori_produksi_makanan hpm, produk p, aset a where hp.waktu_awal= hpm.waktu_awal and hpm.id_produk_makanan = p.id and hpm.id_alat_produksi = a.id and hp.email= %s",[email])
            desc = cursor.description
            nt_result = namedtuple('Hasil_Panen', [col[0] for col in desc])
            result = [nt_result(*row) for row in cursor.fetchall()]

            number_result = {}
            
            sum_of_entitites = range(len(result))
            for i in sum_of_entitites:
                number_result[i+1] = result[i]
            results_pengguna = list(number_result.items())

            # print(number_result)
            cursor.execute("SET search_path TO public")
            return render(request, 'read_histori_produk_makanan.html', {'role': role, 'results_pengguna':results_pengguna })
    return redirect("home:login")

#details produksi
def produksi_details(request, slug):
    # print(x)
    cursor = connection.cursor()
    cursor.execute("SET search_path TO hidayf02")
    cursor.execute("SELECT p.nama, a.nama as nama_aset, pr.durasi, pr.jumlah_unit_hasil, p.id FROM PRODUK p, aset a, produksi pr WHERE p.id = pr.id_produk_makanan AND a.id = pr.id_alat_produksi and p.id =  %s", [slug] )
    object_detail = cursor.fetchone()
 
    id_produk = object_detail[4]
    x = cursor.execute("select id_produk_makanan, p.nama as bahan, jumlah from produk_dibutuhkan_oleh_produk_makanan, produk p where id_produk = p.id AND id_produk_makanan = %s" ,[id_produk])
    desc = cursor.description
    nt_result = namedtuple('Produk', [col[0] for col in desc])
    result = [nt_result(*row) for row in cursor.fetchall()]

    number_result = {}
    cursor.execute('SET search_path TO public')
    
    sum_of_entitites = range(len(result))
    for i in sum_of_entitites:
        number_result[i+1] = result[i]
    x = list(number_result.items())
  
    context = {
        'nama_produk' : object_detail[0],
        'alat_produki' :object_detail[1],
        'durasi' : object_detail[2],
        'jumlah' : object_detail[3],
        
    }

    cursor.execute('SET search_path TO public')
    return render(request, 'details_produksi.html', {'object' : context, 'object_bahan':x } )
  
# produksi update
def update_produksi(request, slug):
    # print(x)
    cursor = connection.cursor()
    cursor.execute("SET search_path TO hidayf02")
    cursor.execute("SELECT p.nama, a.nama as nama_aset, pr.durasi, pr.jumlah_unit_hasil, p.id FROM PRODUK p, aset a, produksi pr WHERE p.id = pr.id_produk_makanan AND a.id = pr.id_alat_produksi and p.id =  %s", [slug] )
    object_detail = cursor.fetchone()

    id_produk = object_detail[4]
    x = cursor.execute("select id_produk_makanan, p.nama as bahan, jumlah from produk_dibutuhkan_oleh_produk_makanan, produk p where id_produk = p.id AND id_produk_makanan = %s" ,[id_produk])
    desc = cursor.description
    nt_result = namedtuple('Produk', [col[0] for col in desc])
    result = [nt_result(*row) for row in cursor.fetchall()]

    number_result = {}
    
    sum_of_entitites = range(len(result))
    for i in sum_of_entitites:
        number_result[i+1] = result[i]
    x = list(number_result.items())
  
    context = {
        'nama_produk' : object_detail[0],
        'alat_produki' :object_detail[1],       
    }
    
    
    if request.method == 'POST':
        durasi_produksi = request.POST['durasi_produksi']
        jumlah_produk_yang_dihasilkan = request.POST['jumlah_produk_yang_dihasilkan']
        if durasi_produksi == '' or jumlah_produk_yang_dihasilkan == '':
            print('isi dulu mas')
        else:
            cursor.execute('select id from aset where nama = %s', [object_detail[1]])
            id_aset = cursor.fetchone()[0]
            # print(id_aset)
            cursor.execute('update produksi set durasi = %s, jumlah_unit_hasil = %s where id_produk_makanan = %s and id_alat_produksi = %s', [durasi_produksi,jumlah_produk_yang_dihasilkan,slug,id_aset])
            cursor.execute('SET search_path TO public')
            return redirect('home:produksi')


    cursor.execute('SET search_path TO public')
    return render(request, 'update_produksi.html', {'object' : context, 'object_bahan':x } )

def delete_produksi(request, slug= NONE):
  
    bagi_dua = slug.split('_')
    print(bagi_dua)
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    cursor.execute("SET search_path TO hidayf02")
    cursor.execute("delete from produksi where id_produk_makanan = %s and id_alat_produksi = %s",[bagi_dua[0], bagi_dua[1]])
    cursor.execute("SET search_path TO public")
    return redirect('/produksi')

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

    # sum_of_entitites = range(len(result)-1)
    sum_of_entitites = range(len(result))
    for i in sum_of_entitites:
        number_result[i+1] = result[i]
    
    return list(number_result.items())

def create_produk(request): # membuat produk (admin) user masuk dalam keadaan sudah pasti login
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    cursor.execute("SET search_path TO hidayf02")

    if request.method == 'POST':
        # try:
        selected = request.POST.get('selected','') #kalau kosong hasilnya True
        nama = request.POST['nama']  
        harga_jual = request.POST['harga_jual']
        sifat_produk = request.POST['sifat_produk']
        try:
            if(selected == '' or nama == '' or harga_jual == '' or sifat_produk == ''):
                print('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')
                messages.error(request, 'Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')
            else:
                if(selected == 'hasil_panen'):
                    cursor.execute("SELECT max(NULLIF(regexp_replace(id, '\D','','g'), '')::numeric) from produk where id like 'hp%'")
                    max_id_hp = cursor.fetchone()[0]
                    # print(max_id_hp)
                    cursor.execute("INSERT INTO produk VALUES(%s,%s,%s,%s)",["hp"+str(max_id_hp+1),nama,harga_jual,sifat_produk])
                elif(selected == 'produk_hewan'):
                    cursor.execute("SELECT max(NULLIF(regexp_replace(id, '\D','','g'), '')::numeric) from produk where id like 'ph%'")
                    max_id_ph = cursor.fetchone()[0]
                    # print(max_id_hp)
                    cursor.execute("INSERT INTO produk VALUES(%s,%s,%s,%s)",["hp"+str(max_id_ph+1),nama,harga_jual,sifat_produk])
                else: # produk_makanan
                    cursor.execute("SELECT max(NULLIF(regexp_replace(id, '\D','','g'), '')::numeric) from produk where id like 'pm%'")
                    max_id_pm = cursor.fetchone()[0]
                    # print(max_id_hp)
                    cursor.execute("INSERT INTO produk VALUES(%s,%s,%s,%s)",["pm"+str(max_id_pm+1),nama,harga_jual,sifat_produk])
                cursor.execute("SET search_path TO public")
                return redirect('home:produk')
        except:
            messages.error(request, 'Inputan harga jual harus berupa integer')
            print('Inputan harga jual harus berupa integer')
    cursor.execute("SET search_path TO public")
    return render(request, 'create_produk.html')

def update_produk(request, slug): # membuat produk (admin)
    # bagi_dua = slug.slit('_')
    # print(bagi_dua)
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    cursor.execute("SET search_path TO hidayf02")
    # object_admin = object_entitas('SELECT id,nama,harga_jual,sifat_produk, CASE WHEN id LIKE ' + "'%hp%'" + ' THEN ' + "'Hasil Panen'" + 'WHEN id LIKE '+ "'%ph%'" + ' THEN ' + "'Produk Hewan'"  + 'WHEN id LIKE ' + "'%pm%'" + 'THEN ' + "'Produk Makanan'" + ' END AS jenis FROM PRODUK')
    cursor.execute('SELECT id,nama,harga_jual,sifat_produk, CASE WHEN id LIKE ' + "'%hp%'" + ' THEN ' + "'Hasil Panen'" + 'WHEN id LIKE '+ "'%ph%'" + ' THEN ' + "'Produk Hewan'"  + 'WHEN id LIKE ' + "'%pm%'" + 'THEN ' + "'Produk Makanan'" + ' END AS jenis FROM PRODUK ')
    # print(cursor.fetchone())
    desc = cursor.description
    nt_result = namedtuple('Produk', [col[0] for col in desc])
    result = [nt_result(*row) for row in cursor.fetchall()]
    # print(result)
    content = ''
    for i in result:
        if(i.id == slug):
            content = i
    
    if request.method == 'POST':
        id = content.id
        nama = content.nama
        harga_jual = request.POST['harga_jual']
        sifat_produk = request.POST['sifat_produk']
        try:
            if(harga_jual == '' or sifat_produk == ''):
                print('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')
                messages.error(request, 'Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')
            else:
                cursor.execute('update produk set harga_jual = %s, sifat_produk = %s where id = %s and nama = %s', [harga_jual,sifat_produk, id, nama])
                cursor.execute("SET search_path TO public")
                return redirect('home:produk')
        except:
            messages.error(request, 'Inputan harga jual harus berupa integer')
            print('Inputan harga jual harus berupa integer')
    cursor.execute("SET search_path TO public")
    return render(request, 'update_produk.html', {'content': content})

def delete_produk(request, slug):
 
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    cursor.execute("SET search_path TO hidayf02")
    cursor.execute("delete from produk where id = %s",[slug])
    cursor.execute("SET search_path TO public")
    return redirect('/produk')
# produksi/delete
# def
def create_produksi(request):
    try:
        cursor = connection.cursor()
        cursor.execute("SET search_path TO public")
        cursor.execute("SET search_path TO hidayf02")
        #1 Produk Makanan
        cursor.execute('select nama  from produk, produk_makanan where id = id_produk')
        desc = cursor.description
        nt_result = ''
        for col in desc:
            nt_result = namedtuple('Produk_Makanan',[col[0]])
        
        result = []
        for row in cursor.fetchall():
            result.append(nt_result(row[0]))

        #2 Produk Aset
        cursor.execute('select nama from aset, alat_produksi where id = id_aset')
        x = cursor.description
        nt_result_sec = ''
        for col in x:
            nt_result_sec = namedtuple('Produk_Aset',[col[0]])
        
        result_sec = []
        for row in cursor.fetchall():
            result_sec.append(nt_result_sec(row[0]))
        # 3 Bahan
        cursor.execute('select nama from produk')
        desc = cursor.description
        nt_result_thrd = ''
        for col in desc:
            nt_result_thrd = namedtuple('Bahan',[col[0]])
        
        result_thrd = []
        for row in cursor.fetchall():
            result_thrd.append(nt_result_thrd(row[0]))

        if request.method == 'POST':
            nama_produk_makanan = request.POST['nama_produk_makanan']
            alat_produksi = request.POST['alat_produksi']
            durasi_produksi = request.POST['durasi_produksi']
            jumlah_produk_dihasilkan = request.POST['jumlah_produk_dihasilkan']
            selected_one = request.POST.get('selected-one','') 
            jumlah_one = request.POST.get('jumlah-one', '')
            selected_two = request.POST.get('selected-two','') 
            jumlah_two = request.POST.get('jumlah-two', '')
            selected_three = request.POST.get('selected-three','')
            jumlah_three = request.POST.get('jumlah-three', '')

            if nama_produk_makanan != '' and alat_produksi != '' and durasi_produksi != '' and jumlah_produk_dihasilkan != '':
                cursor.execute('select id from produk where nama = %s', [nama_produk_makanan])
                id_produk_makanan = cursor.fetchone()[0]
                print(id_produk_makanan)
                cursor.execute('select id from aset where nama = %s', [alat_produksi])
                id_aset = cursor.fetchone()[0]
                print(id_aset)
                cursor.execute('insert into produksi(id_alat_produksi, id_produk_makanan, durasi, jumlah_unit_hasil) values(%s,%s,%s,%s)', [id_aset,id_produk_makanan,durasi_produksi,jumlah_produk_dihasilkan])

                if selected_one != '' and jumlah_one != '':
                    cursor.execute('select id from produk where nama = %s',[selected_one])
                    id_bahan_pertama = cursor.fetchone()[0]
                    cursor.execute('insert into produk_dibutuhkan_oleh_produk_makanan values(%s,%s,%s)',[id_produk_makanan, id_bahan_pertama, jumlah_one])
                if selected_two != '' and jumlah_two != '':
                    cursor.execute('select id from produk where nama = %s',[selected_two])
                    id_bahan_kedua = cursor.fetchone()[0]
                    cursor.execute('insert into produk_dibutuhkan_oleh_produk_makanan values(%s,%s,%s)',[id_produk_makanan, id_bahan_kedua, jumlah_two])
                if selected_three != '' and jumlah_three != '':
                    cursor.execute('select id from produk where nama = %s',[selected_three])
                    id_bahan_ketiga = cursor.fetchone()[0]
                    cursor.execute('insert into produk_dibutuhkan_oleh_produk_makanan values(%s,%s,%s)',[id_produk_makanan, id_bahan_ketiga, jumlah_three])
                cursor.execute("SET search_path TO public")
                return redirect('home:produksi')
    except Exception as e:
        cursor.execute("SET search_path TO public")
        print('SUDAH ADA BOS')
        print(e)

    cursor.execute("SET search_path TO public")
    return render(request, 'create_produksi.html', {'object_makanan' : result, 'object_aset' : result_sec, 'object_bahan' :result_thrd})

def create_histori_produk_makanan(request): # membuat histori produk (pengguna)
    email = request.session['email']
    print(email)
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    cursor.execute("SET search_path TO hidayf02")

    object_produk_makan = object_entitas('select nama, p.id  from produk p, produk_makanan where id = id_produk')
    cursor.execute("SET search_path TO hidayf02")
    if request.method == 'POST':
        selected = request.POST.get('selected','') 
        jumlah = request.POST['jumlah']  
        xp = int(jumlah) * 5
        id_produk_makanan = ''
        for i,j in object_produk_makan:
            if(j.nama == selected):
                id_produk_makanan = j.id
                break
        if(selected == '' or jumlah == ''):
            messages.error(request, 'Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')

        else:
          
            # bahan
            cursor.execute('select id_lumbung, lmp.id_produk as bahan, lmp.jumlah bahan_dimiliki_pengguna, id_produk_makanan, pdop.jumlah bahan_dibutuhkan_produk_makanan from lumbung_memiliki_produk lmp, produk_dibutuhkan_oleh_produk_makanan pdop where lmp.id_produk = pdop.id_produk and id_produk_makanan = %s and id_lumbung = %s', [id_produk_makanan,email[0]])
            desc = cursor.description
            nt_result = namedtuple('Bahan', [col[0] for col in desc])
            result = [nt_result(*row) for row in cursor.fetchall()]
            print(result)

            cursor.execute('select id_koleksi_aset, id_aset, jumlah jumlah_aset, id_produk_makanan, jumlah_unit_hasil from koleksi_aset_memiliki_aset , produksi where id_aset = id_alat_produksi and id_produk_makanan = %s and id_koleksi_aset = %s', [id_produk_makanan,email[0]])
            desc = cursor.description
            nt_result_kedua = namedtuple('Aset', [col[0] for col in desc])
            result_kedua = [nt_result_kedua(*row) for row in cursor.fetchall()]
            print(result_kedua)

            waktu_awal = str(datetime.now())
            waktu_akhir = str(datetime.now())
            if result != [] and result_kedua != []:
                cursor.execute('select xp from pengguna where email = %s', [email[0]])
     
               
                cursor.execute('create table if not exists temporary_total(x integer)')

                cursor.execute('insert into temporary_total values(%s)', [jumlah])
                cursor.execute("INSERT INTO HISTORI_PRODUKSI VALUES (%s,%s,%s,%s,%s)", [email[0],waktu_awal,waktu_akhir,jumlah, xp])                
                cursor.execute("INSERT INTO HISTORI_PRODUKSI_MAKANAN VALUES (%s,%s,%s,%s)", [email[0],waktu_awal, result_kedua[0].id_aset, id_produk_makanan])

                cursor.execute('DROP TABLE temporary_total')
                cursor.execute("SET search_path TO public")
                return redirect('home:produksi')
            # select id_lumbung, lmp.id_produk as bahan, lmp.jumlah bahan_dimiliki_pengguna, id_produk_makanan, pdop.jumlah bahan_dibutuhkan_produk_makanan from lumbung_memiliki_produk lmp, produk_dibutuhkan_oleh_produk_makanan pdop where lmp.id_produk = pdop.id_produk and id_produk_makanan = 'pm4' and id_lumbung = 'opal@bazdat.com';
            # select id_koleksi_aset, id_aset, jumlah jumlah_aset, id_produk_makanan, jumlah_unit_hasil from koleksi_aset_memiliki_aset , produksi where id_aset = id_alat_produksi and id_produk_makanan = 'pm4' and id_koleksi_aset ='opal@bazdat.com';
            # select * from pengguna where email = 'opal@bazdat.com';
            # delete from histori_produksi_makanan where email = 'opal@bazdat.com';
            # select * from lumbung_memiliki_produk where id_lumbung = 'opal@bazdat.com';

    cursor.execute("SET search_path TO public")
    return render(request, 'create_histori_produk_makanan.html', {'object_produk_makan': object_produk_makan})

def register_admin(request): # membuat produk (admin)
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    cursor.execute("SET search_path TO hidayf02")
    # if not request.session.has_key('email'):
    if request.method == 'POST':
        email = request.POST['email']  
        password = request.POST['password']
        print(email)
        print(password)
        # try:
        if email == '':
            print('isi dulu mas/mba')
        else:
            cursor.execute(f"select email from akun where email = '{email}'")
            authen = cursor.fetchone()
            print(authen)
            if cursor.fetchone() is None and password != '':
                cursor.execute("SET search_path TO public")
                cursor.execute("insert into akun values(%s)",[email])
                cursor.execute("insert into admin values( %s, %s)",[email,password])
                request.session['email'] = [email, 'admin']
                # cursor.execute("SET search_path TO public")
                return redirect('home:home')
            else:
                cursor.execute("SET search_path TO public")
                request.session['email'] = [email, 'admin']
                return redirect('home:home')
    cursor.execute("SET search_path TO public")
    return render(request, 'registrasi_admin.html')

def register_pengguna(request): # membuat produk (admin)
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    cursor.execute("SET search_path TO hidayf02")
    if request.method == 'POST':
        email = request.POST['email']  
        password = request.POST['password']
        area = request.POST['area']
        if email == '':
            print('isi dulu mas/mba')
        else:
            cursor.execute(f"select email from akun where email = '{email}'")
            authen = cursor.fetchone()
            print(authen)
            if cursor.fetchone() is None and password != '':
                cursor.execute("SET search_path TO public")
                cursor.execute("insert into akun values(%s)",[email])
                cursor.execute("insert into pengguna values( %s, %s,%s,%s,%s,%s)",[email,password,area,0,0,1])
                request.session['email'] = [email, 'pengguna',area, 0,0,1]
                # cursor.execute("SET search_path TO public")
                return redirect('home:home')
            else:
                cursor.execute("SET search_path TO public")
                request.session['email'] = [email, 'pengguna',area, 0,0,1]
                # cursor.execute("SET search_path TO public")
                return redirect('home:home')
    
    cursor.execute("SET search_path TO public")
    return render(request, 'registrasi_pengguna.html')
