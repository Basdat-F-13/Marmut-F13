from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db import connection, connections
from django.urls import reverse

# Fungsi yang digunakan untuk melakukan login
def login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        print(request.COOKIES.get('login'))
        user, is_label = authenticate(email, password)
        response = HttpResponseRedirect(reverse("Authentication:nav"))
        if(is_label == True):
            response.set_cookie("login", user[0][2])
        else:
            response.set_cookie("login", user[0][0])
        return response
    
    return render(request, 'loginPage.html')

#Fungsi yang digunakan untuk menampilkan halaman depan login
def showAuthNav(request):
    context = {
        'show_navbar' : False,
    }
    return render(request, "authNav.html", context)

#Fungsi yang digunakan untuk menampilkan navbar utama
def showNav(request):
    email = request.COOKIES.get("login")
    context = get_user_data(email)

    return render(request, "base.html", context)

#Fungsi yang digunakan untuk memproses logout
def logout(request):
    response = HttpResponseRedirect(reverse('Authentication:auth_nav'))
    response.delete_cookie('email')
    
    return response

#Fungsi yang digunakan untuk memproses query SELECT
def selectQuery(query):
    SET_QUERY =  "SET search_path to marmut;"
    query = SET_QUERY + query
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        
        return result
    
#Fungsi yang digunakan untuk memproses query INSERT, DELETE, UPDATE
def modifyQuery(query):
    SET_QUERY =  "SET search_path to marmut;"
    query = SET_QUERY + query
    with connection.cursor() as cursor:
        cursor.execute(query)

#Fungsi yang digunakan untuk mengambil role dari pengguna berdasarkan email
def checkRole(email):
    artist, songwriter, podcaster, label = False, False, False, False
    hak_cipta_artist, hak_cipta_songwriter, hak_cipta_podcaster, hak_cipta_label = "", "", "", ""
    LABEL_QUERY = f"""
        SELECT * FROM LABEL
        WHERE email = '{email}'
    """
    user = selectQuery(LABEL_QUERY)
    print(user)
    if(len(user) != 0):
        label = True
        hak_cipta_label = user[0][2]
        return {'artist':artist, 'songwriter':songwriter, 'podcaster':podcaster, 'label':label, 'hak_cipta':{'artist' : hak_cipta_artist, 'songwriter' : hak_cipta_songwriter, 'podcaster' : hak_cipta_podcaster, 'label' : hak_cipta_label}}

    ARTIST_QUERY = f"""
        SELECT * FROM ARTIST
        WHERE email_akun = '{email}'
    """
    user = selectQuery(ARTIST_QUERY)
    if (len(user) != 0):
        artist = True 
        hak_cipta_artist = user[0][2]

    SONGWRITER_QUERY = f"""
        SELECT * FROM SONGWRITER
        WHERE email_akun = '{email}'
    """
    user = selectQuery(SONGWRITER_QUERY)
    if (len(user) != 0):
        songwriter = True 
        hak_cipta_songwriter = user[0][2]
        
    PODCASTER_QUERY = f"""
        SELECT * FROM PODCASTER
        WHERE email = '{email}'
    """
    user = selectQuery(PODCASTER_QUERY)
    if (len(user) != 0):
        podcaster = True 
        hak_cipta_podcaster = user[0][2]

    return {'artist':artist, 'songwriter':songwriter, 'podcaster':podcaster, 'label':label, 'hak_cipta':{'artist' : hak_cipta_artist, 'songwriter' : hak_cipta_songwriter, 'podcaster' : hak_cipta_podcaster, 'label' : hak_cipta_label}}

#Fungsi yang digunakan untuk mengambil data user dan kembalikan dalam dictionary
def get_user_data (email):
    print("email anda adalah", email)
    context = {}
    USER_QUERY = f"""
        SELECT * FROM AKUN
        WHERE email = '{email}'
    """

    LABEL_QUERY = f"""
        SELECT * FROM LABEL
        WHERE email = '{email}'
    """
    user = selectQuery(USER_QUERY)
    if (len(user) != 0):
        context = {
            "show_navbar" : True,
            "user_email" : user[0][0],
            "user_password" : user[0][1],
            "user_name" : user[0][2],
            "user_gender" : 'Female' if user[0][3] == 0 else 'Male',
            "user_tempat_lahir" : user[0][4],
            "user_tanggal_lahir" : user[0][5],
            "user_is_verified" : user[0][6],
            "user_kota_asal" : user[0][7],
            "user_role" : checkRole(email=user[0][0])
        }
    else:
        user = selectQuery(LABEL_QUERY)
        context = {
            "show_navbar" : True, 
            "user_id" : user[0][0],
            "user_name" : user[0][1],
            "user_email" : user[0][2],
            "user_password" : user[0][3],
            "user_kontak" : user[0][4],
            "user_role" : checkRole(email=user[0][2])
        }
    return context

def authenticate(email, password):
    USER_QUERY = f"""
        SELECT * FROM  AKUN
        WHERE email = '{email}' AND password = '{password}';
    """

    LABEL_QUERY = f"""
        SELECT * FROM LABEL
        WHERE email = '{email}' AND password = '{password}';
    """

    user = selectQuery(USER_QUERY)
    if (len(user) != 0):
        label = False
        return user, label
    else:
        user = selectQuery(LABEL_QUERY)
        label = True
        return user, label

#Fungsi yang digunakan untuk mengecek apakah pengguna Premium
def check_premium(email):
    SUBSCRIPTION_QUERY = f"""
        SELECT * FROM PREMIUM 
        WHERE email = '{email}'
    """
    
def showRegister(request):
    context = {
        'show_navbar' : False,
    }
    return render(request, "register.html", context)

def showUserRegPage(request):
    context = {
        'show_navbar' : False,
        'user' : True,
        'label' : False
    }
    return render(request, "userReg.html", context)

def showLabelRegPage(request):
    context = {
        'show_navbar' : False,
        'user' : False,
        'label' : True
    }
    return render(request, "labelReg.html", context)
