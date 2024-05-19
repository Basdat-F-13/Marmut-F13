from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db import connection as conn
from datetime import date
import uuid

def showManagePlaylistPage(request):
    email = request.COOKIES.get("login")

    with conn.cursor() as cursor:
        try:
            cursor.execute("Set search_path to marmut;")
            cursor.execute("SELECT * FROM USER_PLAYLIST WHERE email_pembuat = %s", [email])
            rows = cursor.fetchall()
            playlists = [
                {
                'id':row[1],
                'judul': row[2],
                'jumlah_lagu': row[4],
                'total_durasi': row[7],
                }
                for row in rows
            ]

            context = {
                'playlists': playlists,
                'show_navbar': True,
            }

            
        except:
            context = {
                'show_navbar': True,
            }
            print('belum ada playlist')

    return render(request, "manageplaylist.html", context)

def add_playlist(request):
    if request.method == "POST":
        email = request.COOKIES.get("login")
        id_user_playlist = str(uuid.uuid4())
        judul = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')
        id_playlist = str(uuid.uuid4())


        with conn.cursor() as cursor:
            cursor.execute("Set search_path to marmut;")
            cursor.execute("""
                INSERT INTO PLAYLIST (id)
                VALUES (%s)
            """,[id_playlist])
            
            cursor.execute("""
                INSERT INTO USER_PLAYLIST (email_pembuat, id_user_playlist, judul, deskripsi, jumlah_lagu, tanggal_dibuat, id_playlist, total_durasi)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, [email, id_user_playlist, judul, deskripsi,0, date.today(),id_playlist,0])

            return redirect('manageplaylist:manage-playlist')

def edit_playlist(request, id_playlist):
    if request.method == "POST":
        judul = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')

        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE USER_PLAYLIST
                SET judul = %s, deskripsi = %s
                WHERE id_user_playlist = %s
            """, [judul, deskripsi, id_playlist])

            print('berhasil!!')
            return redirect('manageplaylist:manage-playlist')



def delete_playlist(request, id_playlist):
    with conn.cursor() as cursor:
        cursor.execute("Set search_path to marmut;")
        cursor.execute("SELECT * FROM USER_PLAYLIST WHERE id_user_playlist = %s", [id_playlist])
        rows = cursor.fetchone()

        id = rows[6]

        cursor.execute("""
            DELETE FROM USER_PLAYLIST
            WHERE id_user_playlist = %s
        """, [id_playlist])

        cursor.execute("""
            DELETE FROM playlist
            WHERE id = %s
        """, [id])
        return redirect('manageplaylist:manage-playlist')

def showPlaylistPage(request, id_playlist):
    with conn.cursor() as cursor:
        try:
            cursor.execute("Set search_path to marmut;")
            cursor.execute("SELECT * FROM USER_PLAYLIST WHERE id_user_playlist = %s", [id_playlist])
            row = cursor.fetchone()

            email = row[0]

            cursor.execute("SELECT nama FROM AKUN WHERE email = %s", [email])
            pembuat = cursor.fetchone()[0]

            cursor.execute("""
                SELECT konten.judul, akun.nama, song.id_konten, konten.durasi
                FROM USER_PLAYLIST AS UP
                JOIN PLAYLIST_SONG AS PS ON UP.id_playlist = PS.id_playlist
                JOIN KONTEN ON PS.id_song = konten.id
                JOIN SONG ON PS.id_song = SONG.id_konten
                JOIN ARTIST ON SONG.id_artist = ARTIST.id
                JOIN AKUN ON ARTIST.email_akun = AKUN.email
                WHERE UP.id_user_playlist = %s;
            """, [id_playlist])
            songs = cursor.fetchall()

            detail = {
                'judul': row[2],
                'pembuat': pembuat,
                'jumlah_lagu': row[4],
                'total_durasi': row[7],
                'tanggal_dibuat':row[5],
                'deskripsi':row[3],
                'id_playlist': row[6],
            }

            song_list = [
                {
                    'judul': song[0],
                    'artist': song[1],
                    'id_konten': song[2],
                    'durasi': song[3]
                } for song in songs
            ]

            cursor.execute("""
                SELECT konten.judul, akun.nama, song.id_konten
                FROM SONG
                JOIN KONTEN ON SONG.id_konten = KONTEN.id
                JOIN ARTIST ON SONG.id_artist = ARTIST.id
                JOIN AKUN ON ARTIST.email_akun = AKUN.email;
            """)
            all_songs = cursor.fetchall()

            all_songs = [
                {
                    'judul': song[0],
                    'artist': song[1],
                    'id_konten': song[2],
                } for song in all_songs
            ]

            return render(request,"userplaylistdetail.html",{'detail' : detail, 'songs': song_list, 'all_songs':all_songs} )
            
        except Exception as e:
            msg = str(e).split('\n')[0]
            print( f' gagal: {msg}')
            return render(request,"userplaylistdetail.html",{} )

def add_song(request, id_playlist):
    if request.method == "POST":
        id_lagu = request.POST.get('song')

        with conn.cursor() as cursor:
            cursor.execute("Set search_path to marmut;")

            cursor.execute("""
                INSERT INTO PLAYLIST_SONG (id_playlist, id_song)
                VALUES (%s, %s)
            """, [id_playlist, id_lagu])

            cursor.execute("""
                SELECT COUNT(id_song)
                FROM PLAYLIST_SONG
                WHERE id_playlist = %s
            """, [id_playlist])
            jumlah_lagu = cursor.fetchone()[0]

            cursor.execute("""
                SELECT SUM(konten.durasi)
                FROM PLAYLIST_SONG
                JOIN SONG ON PLAYLIST_SONG.id_song = SONG.id_konten
                JOIN KONTEN ON konten.id = SONG.id_konten
                WHERE PLAYLIST_SONG.id_playlist = %s
            """, [id_playlist])
            total_durasi = cursor.fetchone()[0]

            cursor.execute("""
                UPDATE USER_PLAYLIST
                SET jumlah_lagu = %s, total_durasi = %s
                WHERE id_user_playlist = %s;
            """, [jumlah_lagu, total_durasi, id_playlist])

        return redirect('manageplaylist:manage-playlist')

def showPlayingSongPage(request, id_konten):
    with conn.cursor() as cursor:
        email = request.COOKIES.get("login")

        cursor.execute("Set search_path to marmut;")
        cursor.execute("""
            SELECT 
                konten.judul,
                akun.nama,
                konten.durasi,
                konten.tanggal_rilis,
                konten.tahun,    
                song.total_play,
                song.total_download,
                album.judul
            FROM 
                konten
            JOIN 
                song ON konten.id = song.id_konten
            JOIN
                album ON album.id = song.id_album
            JOIN
                artist ON artist.id = song.id_artist
            JOIN
                akun ON akun.email = artist.email_akun
            WHERE 
                konten.id = %s;
        """, [id_konten])
        song = cursor.fetchone()

        cursor.execute("""
            SELECT GENRE.genre
            FROM GENRE
            JOIN konten ON konten.id = GENRE.id_konten
            WHERE  konten.id = %s;
        """, [id_konten])
        genres = cursor.fetchall()

        cursor.execute("""
            SELECT  AKUN.nama
            FROM AKUN
            JOIN songwriter ON songwriter.email_akun = akun.email
            JOIN songwriter_write_song ON songwriter_write_song.id_songwriter = songwriter.id
            JOIN song ON song.id_konten = songwriter_write_song.id_song
            WHERE song.id_konten = %s;
        """, [id_konten])
        songwriters = cursor.fetchall()

        detail = {
            'id_song' : id_konten,
            'judul' : song[0],
            'genres' : [
                {
                    'genre': genre[0]
                } for genre in genres
            ],
            'artist': song[1],
            'songwriters': [
                {
                    'songwriter' : songwriter[0]
                } for songwriter in songwriters
            ],
            'durasi': song[2],
            'tanggal_rilis': song[3],
            'tahun': song[4],
            'total_play': song[5],
            'total_download': song[6],
            'album': song[7],
        }

        cursor.execute("""
            SELECT premium.email
            FROM premium
            WHERE premium.email = %s;
        """, [email])
        is_premium = cursor.fetchone()

        cursor.execute("""
            SELECT judul, id_user_playlist
            FROM USER_PLAYLIST
            WHERE email_pembuat = %s;
        """, [email])

        playlists = cursor.fetchall()

        playlists = [
            {
                'playlist' : playlist[0],
                'id': playlist[1]
            } for playlist in playlists
        ]

        context = {
            'detail': detail,
            'playlists': playlists,
            'show_navbar': True,
        }
        if is_premium:
            context = {
                'detail': detail,
                'premium':'premium',
                'playlists': playlists,
                'show_navbar': True,
            }
        


    return render(request,"playsong.html",context)

def add_song_to_playlist(request, id_konten):
    if request.method == "POST":
        with conn.cursor() as cursor:
            email = request.COOKIES.get("login")
            id_user_playlist = request.POST.get('playlist')

            cursor.execute("Set search_path to marmut;")
            cursor.execute("""
                SELECT konten.judul, akun.nama
                FROM SONG
                JOIN KONTEN ON SONG.id_konten = KONTEN.id
                JOIN ARTIST ON SONG.id_artist = ARTIST.id
                JOIN AKUN ON ARTIST.email_akun = AKUN.email
                WHERE KONTEN.id = %s;
            """, [id_konten])

            song = cursor.fetchone()

            cursor.execute("""
                SELECT id_playlist
                FROM USER_PLAYLIST
                WHERE id_user_playlist = %s;
            """, [id_user_playlist])
            id_playlist = cursor.fetchone()

            cursor.execute("""
                INSERT INTO PLAYLIST_SONG (id_playlist, id_song)
                VALUES (%s, %s)
            """, [id_playlist, id_konten])

            cursor.execute("""
                SELECT COUNT(id_song)
                FROM PLAYLIST_SONG
                WHERE id_playlist = %s
            """, [id_playlist])
            jumlah_lagu = cursor.fetchone()[0]

            cursor.execute("""
                SELECT SUM(konten.durasi)
                FROM PLAYLIST_SONG
                JOIN SONG ON PLAYLIST_SONG.id_song = SONG.id_konten
                JOIN KONTEN ON konten.id = SONG.id_konten
                WHERE PLAYLIST_SONG.id_playlist = %s
            """, [id_playlist])
            total_durasi = cursor.fetchone()[0]

            cursor.execute("""
                UPDATE USER_PLAYLIST
                SET jumlah_lagu = %s, total_durasi = %s
                WHERE id_user_playlist = %s;
            """, [jumlah_lagu, total_durasi, id_playlist])

        return redirect('manageplaylist:manage-playlist')
            
def delete_song(request, id_playlist, id_konten):
    with conn.cursor() as cursor:
        cursor.execute("Set search_path to marmut;")
        cursor.execute("SELECT * FROM USER_PLAYLIST WHERE id_user_playlist = %s", [id_playlist])
        row = cursor.fetchone()

        cursor.execute("""
            DELETE FROM PLAYLIST_SONG
            WHERE id_playlist = %s AND id_song = %s
        """, [id_playlist, id_konten])

        cursor.execute("""
            SELECT COUNT(id_song)
            FROM PLAYLIST_SONG
            WHERE id_playlist = %s
        """, [id_playlist])
        jumlah_lagu = cursor.fetchone()[0]

        cursor.execute("""
            SELECT SUM(konten.durasi)
            FROM PLAYLIST_SONG
            JOIN SONG ON PLAYLIST_SONG.id_song = SONG.id_konten
            JOIN KONTEN ON konten.id = SONG.id_konten
            WHERE PLAYLIST_SONG.id_playlist = %s
        """, [id_playlist])
        total_durasi = cursor.fetchone()[0]

        cursor.execute("""
                UPDATE USER_PLAYLIST
                SET jumlah_lagu = %s, total_durasi = %s
                WHERE id_user_playlist = %s;
            """, [jumlah_lagu, total_durasi, id_playlist])
        
        return redirect('manageplaylist:manage-playlist')
