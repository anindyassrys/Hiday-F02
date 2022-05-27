from django.shortcuts import render
from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.db import connection
from collections import namedtuple

# Create your views here.

def tuple_fetch(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def list_histori_penjualan(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        result = []
        try:
            cursor.execute("set search_path to hidayf02")
            if (request.session['email'][1] == 'admin'):
                cursor.execute("select * from histori_penjualan;")
                result = tuple_fetch(cursor)
                role = "admin"

            else:
                cursor.execute("select * from histori_penjualan where email = '"+ request.session['email'][0] +"'")
                result = tuple_fetch(cursor)
                role = "pengguna"

        except Exception as e:
            print(e)
        
        finally:
            cursor.close()

        return render(request, 'list_histori_penjualan.html', {"result" : result, "role" : role})

    else:
        return HttpResponseRedirect('/login')

def detail_penjualan(request, email, id):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        result1 = []
        result2 = []
        result3 = []
        try:
            cursor.execute("set search_path to hidayf02")
            if (request.session['email'][1] == 'admin'):
                role = "admin"

            else:
                role = "pengguna"

            cursor.execute("select email, waktu_penjualan from histori_penjualan where id_pesanan = '" + id +"' and email = '"+ email +"';")
            result1 = tuple_fetch(cursor)

            cursor.execute("select id, nama, jenis, total, status from pesanan where id = '" + id +"';")
            result2 = tuple_fetch(cursor)

            cursor.execute("select p.nama, dp.jumlah, dp.subtotal from detail_pesanan dp join produk p on dp.id_produk = p.id where dp.id_pesanan = '" + id +"';")
            result3 = tuple_fetch(cursor)       

        except Exception as e:
            print(e)
        
        finally:
            cursor.close()

        return render(request, 'detail_penjualan.html', {"result1" : result1, "result2" : result2, "result3" : result3, "role":role})

    else:
        return HttpResponseRedirect('/login')
