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

def list_histori_pesanan(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        result1 = []
        result2 = []
        result3 = []
        try:
            cursor.execute("set search_path to hidayf02")
            if (request.session['email'][1] == 'admin'):
                cursor.execute("select * from pesanan where id in (select id_pesanan from histori_penjualan) order by id asc;")
                result2 = tuple_fetch(cursor)
                cursor.execute("select * from pesanan where id not in (select id_pesanan from histori_penjualan) order by id asc;")
                result3 = tuple_fetch(cursor)
                role = "admin"

            else:
                cursor.execute("select * from pesanan order by id asc;")
                result1 = tuple_fetch(cursor)
                role = "pengguna"

        except Exception as e:
            print(e)
        
        finally:
            cursor.close()

        return render(request, 'list_histori_pesanan.html', {"result1" : result1, "result2" : result2, "result3" : result3, "role" : role})

    else:
        return HttpResponseRedirect('/login')

def detail_pesanan(request, id):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        result1 = []
        result2 = []
        try:
            cursor.execute("set search_path to hidayf02")
            cursor.execute("select id, nama, jenis, total, status from pesanan where id = '" + id +"';")
            result1 = tuple_fetch(cursor)
            cursor.execute("select p.nama, dp.jumlah, dp.subtotal from detail_pesanan dp join produk p on dp.id_produk = p.id where dp.id_pesanan = '" + id +"';")
            result2 = tuple_fetch(cursor)

            if (request.session['email'][1] == 'admin'):
                role = "admin"

            else:
                role = "pengguna"
                if request.method == "POST":
                    id = request.POST["id"]
                    total = request.POST["total"]
                    cursor.execute("select (now() + interval '7 hours')::timestamp")
                    ts = tuple_fetch(cursor)
                    time_str = str(ts[0][0])
                    cursor.execute("insert into histori_penjualan values ('"+ request.session['email'][0] +"',  '" + time_str + "'::timestamp,'"+ total +"', 10, '"+ id +"' )")
                    return HttpResponseRedirect('/histori-penjualan/list-histori-penjualan')

        except Exception as e:
            print(e)
        
        finally:
            cursor.close()

        return render(request, 'detail_pesanan.html', {"result1" : result1, "result2" : result2, "role" : role})

    else:
        return HttpResponseRedirect('/login')

def create_pesanan(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        try:
            cursor.execute("set search_path to hidayf02")
            if (request.session['email'][1] == 'admin'):
                cursor.execute("select count(id) from pesanan;")
                new_int = int(tuple_fetch(cursor)[0][0]+1)
                new_id = "PS0" + str(new_int)
                cursor.execute("select * from produk")
                result = tuple_fetch(cursor)

            if request.method == "POST":
                res_post = request.POST.dict()
                res_post.pop("csrfmiddlewaretoken")
                # cursor.execute("insert into pesanan values('" + new_id + "', 'diproses', '" + res_post["jenis"] + "', '" + res_post["nama_pesanan"] + "', 0)")
                # res_post.pop("nama_pesanan")
                # res_post.pop("jenis")
                no_urut = 1
                count = 0

                jenis_insert = res_post["jenis"]
                nama_insert = res_post["nama_pesanan"]
                res_post.pop("nama_pesanan")
                res_post.pop("jenis")

                for i in res_post:
                    if int(res_post.get(i)) > 0:
                        count = count + 1

                if count == 0:
                    messages.warning(request, "Pilih setidaknya 1 produk dengan jumlah lebih besar dari 0")

                else:
                    cursor.execute("insert into pesanan values('" + new_id + "', 'diproses', '" + jenis_insert + "', '" + nama_insert + "', 0)")
                    for i in res_post:
                        if int(res_post.get(i)) > 0:
                            cursor.execute("select harga_jual from produk where id = '" + i + "'")
                            res = tuple_fetch(cursor)
                            harga_jual = int(res[0][0])
                            subtotal = int(res_post.get(i))*harga_jual
                            cursor.execute("insert into detail_pesanan values('" + new_id + "', " + str(no_urut) + ", " + str(subtotal) + ", " + str(res_post.get(i)) + ", '" + i + "')")
                            no_urut = no_urut+1
                    return HttpResponseRedirect('/pesanan/list-pesanan')

        except Exception as e:
            print(e)

        finally:
            cursor.close()

        return render(request, 'create_pesanan.html', {"new_id" : new_id, "result" : result})
    
    else:
        return HttpResponseRedirect('/login')

def delete_pesanan(request, id):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        try:
            cursor.execute("set search_path to hidayf02")
            cursor.execute("delete from pesanan where id = '" + id + "'")

        except Exception as e:
            print(e)
        
        finally:
            cursor.close()

        return HttpResponseRedirect('/pesanan/list-pesanan')

    else:
        return HttpResponseRedirect('/login')

def update_pesanan(request, id):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        result1 = []
        result2 = []
        try:
            cursor.execute("set search_path to hidayf02")
            cursor.execute("select id, nama, jenis, total, status from pesanan where id = '" + id +"';")
            result1 = tuple_fetch(cursor)
            cursor.execute("select p.nama, dp.jumlah, dp.subtotal from detail_pesanan dp join produk p on dp.id_produk = p.id where dp.id_pesanan = '" + id +"';")
            result2 = tuple_fetch(cursor)

            if request.method == 'POST':
                nama = request.POST["nama"]
                jenis = request.POST["jenis"]
                status = request.POST["status"]

                cursor.execute("update pesanan set nama = '" + nama + "', jenis = '" + jenis + "', status = '" + status + "' where id = '" + id + "'")
                return HttpResponseRedirect('/pesanan/list-pesanan')

        except Exception as e:
            print(e)
        
        finally:
            cursor.close()

        return render(request, 'update_pesanan.html', {"result1" : result1, "result2" : result2})

    else:
        return HttpResponseRedirect('/login')