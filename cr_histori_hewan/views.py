from django.shortcuts import render
from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.db import connection
from collections import namedtuple
from django.contrib import messages

# Create your views here.

def tuple_fetch(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def list_histori_hewan(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        result = []

        try:
            cursor.execute("SET SEARCH_PATH TO hidayf02")
            if (request.session['email'][1] == "admin"):
                cursor.execute("select hp.email, hp.waktu_awal, hp.waktu_selesai, hp.jumlah, hp.xp, a.nama from histori_produksi hp JOIN histori_hewan hh on hp.email = hh.email and hp.waktu_awal = hh.waktu_awal JOIN hewan h on hh.id_hewan = h.id_aset JOIN aset a on h.id_aset = a.id;")
                result = tuple_fetch(cursor)
                role = "admin"

            else:
                cursor.execute("select hp.waktu_awal, hp.waktu_selesai, hp.jumlah, hp.xp, a.nama from histori_produksi hp JOIN histori_hewan hh on hp.email = hh.email and hp.waktu_awal = hh.waktu_awal JOIN hewan h on hh.id_hewan = h.id_aset JOIN aset a on h.id_aset = a.id WHERE hh.email = '"+ request.session['email'][0] +"'")
                result = tuple_fetch(cursor)
                role = "pengguna"

        except Exception as e:
            print(e)
        
        finally:
            cursor.close()
     
        return render(request, 'list_histori_hewan.html', {"result" : result, "role" : role})

    else:
        return HttpResponseRedirect('/login')

def produksi_hewan(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        result = []

        try:
            cursor.execute("SET SEARCH_PATH TO hidayf02")
            if (request.session['email'][1] == "admin"):
                role = "admin"

            elif (request.session['email'][1] == "pengguna"):
                cursor.execute("select a.nama, kama.id_aset, kama.jumlah from koleksi_aset_memiliki_aset kama join aset a on kama.id_aset = a.id where id_koleksi_aset = '"+ request.session['email'][0] +"' and id in (select id_aset from hewan);")
                result = tuple_fetch(cursor)
                role = "pengguna"

                if request.method == 'POST':
                    nama = request.POST['nama']
                    jumlah = int(request.POST['jumlah'])
                    xp = jumlah*5

                    for i in result:
                        if i[0] == nama:
                            id_hewan = i[1]
                            jumlah_hewan = i[2]

                            if jumlah > jumlah_hewan:
                                messages.warning(request, "Anda tidak memiliki hewan yang cukup, silahkan membeli hewan terlebih dahulu")

                            else:
                                cursor.execute("select (now() + interval '7 hours')::timestamp")
                                ts = tuple_fetch(cursor)
                                time_str = str(ts[0][0])
                                cursor.execute("insert into histori_produksi values('" + request.session['email'][0] + "', '" + time_str + "'::timestamp, '" + time_str + "'::timestamp, " + str(jumlah) + ", " + str(xp) + ")")
                                cursor.execute("insert into histori_hewan values('" + request.session['email'][0] + "', '" + time_str + "'::timestamp, '" + id_hewan + "')")
                                return HttpResponseRedirect('/histori-hewan/list-histori-hewan')

        except Exception as e:
            print(e)
        
        finally:
            cursor.close()
        
        return render(request, 'produksi_hewan.html', {"role" : role, "result" : result})

    else:
        return HttpResponseRedirect('/login')