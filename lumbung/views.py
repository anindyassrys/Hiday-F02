from django.shortcuts import redirect, render
from django.db import connection
from django.contrib import messages

#create upgrade lumbung
def upgrade_lumbung(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        cursor.execute("SET search_path TO hidayf02")
        role = request.session['email'][1]

        if role == "pengguna":
            cursor.execute("SELECT * FROM lumbung WHERE email = '" + request.session['email'][0] + "'")
            result = cursor.fetchall()
            level = result[0][1] + 1
            kapasitas = result[0][2] + 50

            if request.method == "POST":
                cursor.execute("SET search_path to hidayf02")
                cursor.execute("SELECT (NOW() + interval '7 hours')::timestamp")
                result_time = cursor.fetchall()
                time = str(result_time[0][0])

                cursor.execute("SELECT koin FROM pengguna WHERE email = '" + request.session['email'][0] + "'")
                koin_pengguna = cursor.fetchall()
                print(koin_pengguna[0][0])

                if koin_pengguna[0][0] < 200:
                    messages.info(request, "Koin kamu tidak cukup!")
                    return redirect("/lumbung/upgrade-lumbung")

                else:
                    cursor.execute("UPDATE lumbung SET level = %s, kapasitas_maksimal = %s where email = %s", [level, kapasitas, request.session['email'][0]])
                    cursor.execute("INSERT INTO transaksi_upgrade_lumbung VALUES ('"+request.session['email'][0]+"', '"+ time + "')")
                    return redirect("lumbung:list_transaksi_upgrade_lumbung")

            else:
                return render(request, 'upgrade_lumbung.html', {'results' : result, 'level': level, 'role': role, 'kapasitas' : kapasitas})
        else:
            return redirect("lumbung:list_transaksi_upgrade_lumbung")
    else:
        return redirect("home:login")

#read upgrade lumbung
def list_transaksi_upgrade_lumbung(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('email'):
        cursor.execute("SET search_path TO hidayf02")

        if (request.session['email'][1] == "admin"):
            cursor.execute("SELECT * FROM transaksi_upgrade_lumbung")
            result = cursor.fetchall()
            role = "admin"
        else:
            cursor.execute("SELECT * FROM transaksi_upgrade_lumbung WHERE email = '" + request.session['email'][0] + "'")
            result = cursor.fetchall()
            role = "pengguna"
    return render(request, 'list_transaksi_upgrade_lumbung.html', {'results': result, 'role': role})
