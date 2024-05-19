from django.shortcuts import render
from django.db import connection
from Authentication.views import get_user_data

def selectQuery(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to marmut;")
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()

def get_roles(email):
    roles = []
    role_queries = {
        "Artist": "SELECT COUNT(*) FROM ARTIST WHERE email_akun = %s",
        "Songwriter": "SELECT COUNT(*) FROM SONGWRITER WHERE email_akun = %s",
        "Podcaster": "SELECT COUNT(*) FROM PODCASTER WHERE email = %s",
        "Label": "SELECT COUNT(*) FROM LABEL WHERE email = %s"
    }
    for role, query in role_queries.items():
        if selectQuery(query, [email])[0][0] > 0:
            roles.append(role)
    return roles

def get_playlists(email):
    return selectQuery("SELECT id_playlist, judul FROM User_Playlist WHERE email_pembuat = %s", [email])

def get_podcasts(email):
    return selectQuery("""
        SELECT k.id, k.judul
        FROM PODCAST p
        JOIN KONTEN k ON p.id_konten = k.id
        WHERE p.email_podcaster = %s
    """, [email])

def get_songs(email):
    return selectQuery("""
        SELECT k.id, k.judul
        FROM SONG s
        JOIN KONTEN k ON s.id_konten = k.id
        JOIN ARTIST a ON s.email_artist = a.email_akun
        WHERE a.email_akun = %s
    """, [email])

def get_albums(email):
    return selectQuery("""
        SELECT a.id, a.judul
        FROM ALBUM a
        JOIN LABEL l ON a.id_label = l.id
        WHERE l.email = %s
    """, [email])

def showdashboard(request):
    email = request.COOKIES.get("login")
    print("Email from cookies:", email)  # Debug statement
    user = get_user_data(email)
    context = {
        'show_navbar': True
    }

    if user:
        try:
            roles = get_roles(email)
            context['user'] = {
                'email': user.get('user_email', ''),
                'password': user.get('user_password', ''),
                'name': user.get('user_name', ''),
                'gender': user.get('user_gender', ''),
                'tempat_lahir': user.get('user_tempat_lahir', ''),
                'tanggal_lahir': user.get('user_tanggal_lahir', ''),
                'is_verified': user.get('user_is_verified', ''),
                'kota_asal': user.get('user_kota_asal', ''),
            }
            context['roles'] = roles

            if "Label" in roles:
                albums = get_albums(email)
                context['albums'] = albums if albums else "Belum Memproduksi Album"
            if "Artist" in roles or "Songwriter" in roles:
                songs = get_songs(email)
                context['songs'] = songs if songs else "Belum Memiliki Lagu"
            if "Podcaster" in roles:
                podcasts = get_podcasts(email)
                context['podcasts'] = podcasts if podcasts else "Belum Memiliki Podcast"
            if not roles or "User" in roles:
                playlists = get_playlists(email)
                context['playlists'] = playlists if playlists else "Belum Memiliki Playlist"
        except KeyError as e:
            print(f"KeyError: {e}")  # Debug statement
            context['error'] = "Error fetching user data"
    else:
        context['error'] = "No user found"

    return render(request, "dashboard.html", context)
