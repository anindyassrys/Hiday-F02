from django.shortcuts import redirect, render
from django.db import connection
from django.contrib import messages

def produksi_tanaman(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        role = request.session['email'][1]
        cursor.execute("SET search_path to hidayf02")
        if role == "pengguna":
            cursor.execute("SELECT a.nama, kama.id_aset, kama.jumlah FROM koleksi_aset_memiliki_aset kama JOIN aset a ON kama.id_aset = a.id where id_koleksi_aset = '"+ request.session['email'][0] +"' AND id IN (SELECT id_aset FROM bibit_tanaman);")
            bibit_tanaman = cursor.fetchall()
            print(bibit_tanaman)
            cursor.execute("SELECT xp FROM pengguna WHERE email = '" + request.session['email'][0] + "'")
            xp_pengguna = cursor.fetchall()
            xp = 0

            if request.method == "POST":
                nama = request.POST['nama']
                jumlah = int(request.POST['jumlah'])
                xp = jumlah*5

                for i in bibit_tanaman:
                    id_aset = i[1]
                    if i[0] == nama:
                        if i[2] < jumlah:
                            messages.info(request, "Anda tidak memiliki bibit yang cukup, silahkan membeli bibit terlebih dahulu")
                            return redirect("/histori-tanaman/produksi-tanaman")
                        else:
                            cursor.execute("SELECT (NOW() + interval '7 hours')::timestamp")
                            result_time = cursor.fetchall()
                            time = str(result_time[0][0])
                            cursor.execute("INSERT INTO histori_produksi VALUES ('"+request.session['email'][0]+"', '"+ time + "'::timestamp, '"+ time + "'::timestamp, '"+ str(jumlah)+"', '"+str(xp_pengguna[0][0])+"')")
                            cursor.execute("INSERT INTO histori_tanaman VALUES ('"+request.session['email'][0]+"', '"+ time + "'::timestamp, '"+ str(id_aset)+"')")
                            return redirect("histori_tanaman:list_histori_tanaman")
                        
                return redirect("histori_tanaman:list_histori_tanaman")
            else:
                return render(request, 'produksi_tanaman.html', {'bibit_tanaman' : bibit_tanaman, 'xp': xp})
        else:
            return redirect("histori_tanaman:list_histori_tanaman")
    else:
        return redirect("home:login")

def list_histori_tanaman(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        cursor.execute("SET search_path TO hidayf02")

        if (request.session['email'][1] == "admin"):
            cursor.execute("select hp.email, hp.waktu_awal, hp.waktu_selesai, hp.jumlah, hp.xp, a.nama from histori_produksi hp JOIN histori_tanaman ht on hp.email = ht.email and hp.waktu_awal = ht.waktu_awal JOIN bibit_tanaman bt on ht.id_bibit_tanaman = bt.id_aset JOIN aset a on bt.id_aset = a.id;")
            result = cursor.fetchall()
            role = "admin"
        else:
            cursor.execute("select hp.email, hp.waktu_awal, hp.waktu_selesai, hp.jumlah, hp.xp, a.nama from histori_produksi hp JOIN histori_tanaman ht on hp.email = ht.email and hp.waktu_awal = ht.waktu_awal JOIN bibit_tanaman bt on ht.id_bibit_tanaman = bt.id_aset JOIN aset a on bt.id_aset = a.id WHERE hp.email = '" + request.session['email'][0] + "'")
            result = cursor.fetchall()
            role = "pengguna"
        
    return render(request, 'list_produksi_tanaman.html', {'results': result, 'role': role})
