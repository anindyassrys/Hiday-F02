from django.shortcuts import render
from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.db import connection
from collections import namedtuple
from .forms import *

# Create your views here.

def tuple_fetch(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def list_histori_hewan(request):
    if request.session.has_key('email'):
        cursor = connection.cursor()
        result = []

        try:
            cursor.execute("SET SEARCH_PATH TO hidayf02")
            if (request.session['email'][1] == "admin"):
                cursor.execute("select hp.email, hp.waktu_awal, hp.waktu_selesai, hp.jumlah, hp.xp, a.nama from histori_produksi hp JOIN histori_hewan hh on hp.email = hh.email and hp.waktu_awal = hh.waktu_awal JOIN hewan h on hh.id_hewan = h.id_aset JOIN aset a on h.id_aset = a.id;")
                result = tuple_fetch(cursor)
                role = "admin"

            else:
                cursor.execute("select hp.email, hp.waktu_awal, hp.waktu_selesai, hp.jumlah, hp.xp, a.nama from histori_produksi hp JOIN histori_hewan hh on hp.email = hh.email and hp.waktu_awal = hh.waktu_awal JOIN hewan h on hh.id_hewan = h.id_aset JOIN aset a on h.id_aset = a.id WHERE hh.email = '"+ request.session['email'][0] +"'")
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
    if request.session.has_key('email'):
        cursor = connection.cursor()
        result = []

        try:
            cursor.execute("SET SEARCH_PATH TO hidayf02")
            if (request.session['email'][1] == "admin"):
                role = "admin"

            elif (request.session['email'][1] == "pengguna"):
                cursor.execute("select a.nama from aset a join hewan h on a.id = h.id_aset join histori_hewan hh on h.id_aset = hh.id_hewan join pengguna p on hh.email = p.email where p.email = '"+ request.session['email'][0] +"'")
                result = tuple_fetch(cursor)
                role = "pengguna"

        except Exception as e:
            print(e)
        
        finally:
            cursor.close()
        
        # result = [dict(row) for row in result]
        return render(request, 'produksi_hewan.html', {"form" : produksi_hewan_form, "role" : role})

    else:
        return HttpResponseRedirect('/login')