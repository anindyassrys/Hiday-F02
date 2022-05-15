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

def list_histori_pesanan(request):
   if request.session.has_key('email'):
        cursor = connection.cursor()
        result = []
        try:
            cursor.execute("set search_path to hidayf02")
            if (request.session['email'][1] == 'admin'):
                cursor.execute("select * from PESANAN;")
                result = tuple_fetch(cursor)
                role = "admin"

            else:
                cursor.execute("select * from PESANAN;")
                result = tuple_fetch(cursor)
                role = "pengguna"

        except Exception as e:
            print(e)
        
        finally:
            cursor.close()

        return render(request, 'list_histori_pesanan.html', {"result" : result, "role" : role})

   else:
        return HttpResponseRedirect('/login')

def view_detail_pesanan(request, id):
    if request.session.has_key('email'):
        cursor = connection.cursor()
        result1 = []
        result2 = []
        try:
            cursor.execute("set search_path to hidayf02")
            cursor.execute("select id, nama, jenis, total, status from pesanan where id = '" + id +"';")
            result1 = tuple_fetch(cursor)

            if (request.session['email'][1] == 'admin'):
                cursor.execute("select p.nama, dp.jumlah, dp.subtotal from detail_pesanan dp join produk p on dp.id_produk = p.id where dp.id_pesanan = '" + id +"';")
                result2 = tuple_fetch(cursor)
                role = "admin"

            else:
                cursor.execute("select p.nama, dp.jumlah, dp.subtotal from detail_pesanan dp join produk p on dp.id_produk = p.id where dp.id_pesanan = '" + id +"';")
                result2 = tuple_fetch(cursor)
                role = "pengguna"

        except Exception as e:
            print(e)
        
        finally:
            cursor.close()

        return render(request, 'detail_pesanan.html', {"result1" : result1, "result2" : result2, "role" : role})

    else:
        return HttpResponseRedirect('/login')

def create_pesanan(request):
    if (request.session['email'][1] == 'admin'):
        role = "admin"

    else:
        role = "pengguna"
    
    return render(request, 'create_pesanan.html', {"form" : create_pesanan_form, "role" : role})

def update_pesanan(request, id):
    if request.session.has_key('email'):
        cursor = connection.cursor()
        result1 = []
        result2 = []
        try:
            cursor.execute("set search_path to hidayf02")
            cursor.execute("select id, nama, jenis, total, status from pesanan where id = '" + id +"';")
            result1 = tuple_fetch(cursor)

            if (request.session['email'][1] == 'admin'):
                cursor.execute("select p.nama, dp.jumlah, dp.subtotal from detail_pesanan dp join produk p on dp.id_produk = p.id where dp.id_pesanan = '" + id +"';")
                result2 = tuple_fetch(cursor)
                role = "admin"

            else:
                cursor.execute("select p.nama, dp.jumlah, dp.subtotal from detail_pesanan dp join produk p on dp.id_produk = p.id where dp.id_pesanan = '" + id +"';")
                result2 = tuple_fetch(cursor)
                role = "pengguna"

        except Exception as e:
            print(e)
        
        finally:
            cursor.close()

        return render(request, 'update_pesanan.html', {"form": update_pesanan_form, "result1" : result1, "result2" : result2, "role" : role})

    else:
        return HttpResponseRedirect('/login')

