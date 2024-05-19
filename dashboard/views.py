from django.shortcuts import render
from django.db import connection
from Authentication.views import get_user_data
import random


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
        JOIN ARTIST a ON s.id_artist = a.id
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
    context = user
    context ["show_navbar"] = True

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

            images = ['gp1.svg', 'gp2.svg', 'gp3.svg', 'gp4.svg', 'gp5.svg', 'gp6.svg']

            if "Label" in roles:
                albums = get_albums(email)
                if albums:
                    albums_with_images = [(album[0], album[1], random.choice(images)) for album in albums]
                    context['albums'] = albums_with_images
                else:
                    context['albums'] = "Belum Memproduksi Album"
            
            if "Artist" in roles or "Songwriter" in roles:
                songs = get_songs(email)
                if songs:
                    songs_with_images = [(song[0], song[1], random.choice(images)) for song in songs]
                    context['songs'] = songs_with_images
                else:
                    context['songs'] = "Belum Memiliki Lagu"

            if "Podcaster" in roles:
                podcasts = get_podcasts(email)
                if podcasts:
                    podcasts_with_images = [(podcast[0], podcast[1], random.choice(images)) for podcast in podcasts]
                    context['podcasts'] = podcasts_with_images
                else:
                    context['podcasts'] = "Belum Memiliki Podcast"
            
            if not roles or "User" in roles:
                playlists = get_playlists(email)
                if playlists:
                    playlists_with_images = [(playlist[0], playlist[1], random.choice(images)) for playlist in playlists]
                    context['playlists'] = playlists_with_images
                else:
                    context['playlists'] = "Belum Memiliki Playlist"

        except KeyError as e:
            print(f"KeyError: {e}")  # Debug statement
            context['error'] = "Error fetching user data"
    else:
        context['error'] = "No user found"

    return render(request, "dashboard.html", context)
