from django.shortcuts import redirect, render
import random, uuid
from django.contrib import messages
from django.db import connection as conn

# Create your views here.
def showLoginPage(request):
    context = {
        'show_navbar' : False
    }
    return render(request, "loginPage.html", context)

def showAuthNav(request):
    context = {
        'show_navbar' : False,
    }
    return render(request, "authNav.html", context)

def showNav(request):
    context = {
        'show_navbar' : True,
        'premium' : False,
        'user' : True,
        'artist' : False,
        'songwriter' : False,
        'podcast' : True,
        'label' : False
    }
    return render(request, "base.html", context)

def showRegister(request):
    context = {
        'show_navbar' : False,
    }
    return render(request, "register.html", context)

def showUserRegPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        gender = request.POST.get('gender')
        if(gender) == ('Laki-laki'):
            no_gender = 1
        else:
            no_gender = 0
        tempat_lahir = request.POST.get('tempat_lahir')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        kota_asal = request.POST.get('kota_asal')
        roles = request.POST.getlist('role')
        if len(roles) == 1:
            verified = True
        else:
            verified = False

        with conn.cursor() as cursor:
            try:
                cursor.execute("set search_path to marmut;")
                cursor.execute(f"INSERT INTO AKUN(email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal) values ('{email}', '{password}', '{nama}', '{no_gender}', '{tempat_lahir}', '{tanggal_lahir}', '{verified}', '{kota_asal}');")
                for i in roles:
                    if i == "Podcaster":
                        cursor.execute(f"INSERT INTO PODCASTER(email) values ('{email}');")
                    elif i == "Artist":
                        cursor.execute('SELECT * FROM PEMILIK_HAK_CIPTA')
                        hak_cipta = cursor.fetchall()
                        random_hak_cipta = str(random.choice(hak_cipta)[0])
                        id = str(uuid.uuid4())
                        cursor.execute(f"INSERT INTO ARTIST(id, email_akun, id_pemilik_hak_cipta) values ('{id}', '{email}', '{random_hak_cipta}');")
                    elif i == "Songwriter":
                        cursor.execute('SELECT * FROM PEMILIK_HAK_CIPTA')
                        hak_cipta = cursor.fetchall()
                        random_hak_cipta = str(random.choice(hak_cipta)[0])
                        id = str(uuid.uuid4())
                        cursor.execute(f"INSERT INTO SONGWRITER(id, email_akun, id_pemilik_hak_cipta) values ('{id}', '{email}', '{random_hak_cipta}');")
                
                print('Registrasi berhasil!')

            except Exception as e:
                msg = str(e).split('\n')[0]
                print( f'Registrasi gagal: {msg}')
                return render(request, "register_pengguna.html")
            
            context = {
                "is_logged_in": False
            }

            return redirect('Authentication:login')
        
    context = {
        'show_navbar' : False,
        'user' : True,
        'label' : False
    }
    return render(request, "userReg.html", context)

def showLabelRegPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        kontak = request.POST.get('kontak')
        id = str(uuid.uuid4())

        with conn.cursor() as cursor:
            try:
                cursor.execute('set search_path to marmut')
                cursor.execute('SELECT * FROM PEMILIK_HAK_CIPTA')
                hak_cipta = cursor.fetchall()
                random_hak_cipta = str(random.choice(hak_cipta)[0])
                cursor.execute(f"INSERT INTO LABEL(id, nama, email, password, kontak, id_pemilik_hak_cipta) values ('{id}', '{nama}', '{email}', '{password}', '{kontak}', '{random_hak_cipta}')")
            
            except Exception as e:
                msg = str(e).split('\n')[0]
                print( f'Registrasi gagal: {msg}')
                return render(request, "register_label.html")
            
            return redirect('Authentication:login')
            
    context = {
        'show_navbar' : False,
        'user' : False,
        'label' : True,
        'logged_in' : False,
    }
    
    return render(request, "labelReg.html", context)