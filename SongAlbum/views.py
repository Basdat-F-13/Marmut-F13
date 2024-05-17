from django.db import connection
from django.shortcuts import render
from Authentication.views import selectQuery, modifyQuery, checkRole, get_user_data

# Create your views here.
def showAlbumLabel(request):
    email = request.COOKIES.get('login')
    context = get_user_data(email)
    context['albums'] = getAlbumLabel(email)
    return render(request, "manageAlbumLabel.html", context)

def showAlbum(request):
    email = request.COOKIES.get('login')
    context = get_user_data(email)
    context['albums'] = getAlbumLabel(email)
    return render(request, "manageAlbum.html", context)

def showSongLabel(request, album_id):
    email = request.COOKIES.get('login')
    context = get_user_data(email)
    context['songs'] = getAlbumDetail(album_id)
    return render(request, "manageSongLabel.html", context)

def showSong(request):
    context = {
        'show_navbar' : True,
        'user' : True,
        'artist' : True,
        'songwriter' : False,
        'podcast' : False,
        'label' : False
    }
    return render(request, "manageSong.html", context)

def showRoyaltyCheck(request):
    email = request.COOKIES.get('login')
    context = get_user_data(email)
    context['royaltyData'] = getRoyalty(email)
    return render(request, "royaltyCheck.html", context)

def addAlbum(request):
    context = {
        'show_navbar' : True,
        'user' : True,
        'artist' : True,
        'songwriter' : False,
        'podcast' : False,
        'label' : False
    }
    return render(request, 'createAlbum.html', context)

def addSong(request):
    context = {
        'show_navbar' : True,
        'user' : True,
        'artist' : True,
        'songwriter' : False,
        'podcast' : False,
        'label' : False
    }
    return render(request, 'createSong.html', context)

def getAlbums(email):
    ALBUM_QUERY = f"""
        SELECT DISTINCT ALBUM.id, ALBUM.judul AS Judul_Album, ALBUM.jumlah_lagu AS Jumlah_Lagu, ALBUM.total_durasi AS Duration
        FROM ALBUM
        JOIN SONG ON ALBUM.id = SONG.id_album
        JOIN ARTIST ON SONG.id_artist = ARTIST.id
        JOIN SONGWRITER_WRITE_SONG ON SONG.id_konten = SONGWRITER_WRITE_SONG.id_song
        JOIN SONGWRITER ON SONGWRITER_WRITE_SONG.id_songwriter = SONGWRITER.id
        WHERE ARTIST.email_akun = '{email}' OR SONGWRITER.email_akun = '{email}';
    """
    data, col = selectQuery(ALBUM_QUERY), ['ID', 'ALBUM_TITLE', 'COUNT_SONG', 'DURATION']

    colnames = col

    results = [dict(zip(colnames, row)) for row in data]

    return results

def getRoyalty(email):
    ROYALTY_QUERY = f"""
        SELECT  K.judul AS SONG_TITLE, A.judul AS ALBUM_TITLE, S.total_play, S.total_download, PHC.rate_royalti * S.total_play AS royalti_terhitung
        FROM SONG S
        JOIN KONTEN K ON S.id_konten = K.id
        LEFT JOIN ALBUM A ON S.id_album = A.id
        JOIN ARTIST ART ON S.id_artist = ART.id
        JOIN PEMILIK_HAK_CIPTA PHC ON ART.id_pemilik_hak_cipta = PHC.id
        WHERE ART.email_akun = '{email}'
    UNION
        SELECT K.judul AS judul_lagu, A.judul AS judul_album, S.total_play, S.total_download, PHC.rate_royalti * S.total_play AS royalti_terhitung
        FROM SONG S
        JOIN KONTEN K ON S.id_konten = K.id
        LEFT JOIN ALBUM A ON S.id_album = A.id
        JOIN SONGWRITER_WRITE_SONG SWS ON S.id_konten = SWS.id_song
        JOIN SONGWRITER SW ON SWS.id_songwriter = SW.id
        JOIN PEMILIK_HAK_CIPTA PHC ON SW.id_pemilik_hak_cipta = PHC.id
        WHERE SW.email_akun = '{email}'
    UNION
        SELECT K.judul AS judul_lagu, A.judul AS judul_album, S.total_play, S.total_download, PHC.rate_royalti * S.total_play AS royalti_terhitung
        FROM SONG S
        JOIN KONTEN K ON S.id_konten = K.id
        LEFT JOIN ALBUM A ON S.id_album = A.id
        JOIN LABEL L ON A.id_label = L.id
        JOIN PEMILIK_HAK_CIPTA PHC ON L.id_pemilik_hak_cipta = PHC.id
        WHERE L.email = '{email}';
    """
    data, col = selectQuery(ROYALTY_QUERY), ['SONG_TITLE', 'ALBUM_TITLE', 'TOTAL_PLAY', 'TOTAL_DOWNLOAD', 'ROYALTY_RATE']

    colnames = col

    results = [dict(zip(colnames, row)) for row in data]

    return results

def getAlbumLabel(email):
    ALBUM_QUERY = f"""
        SELECT DISTINCT A.id, A.judul, A.jumlah_lagu, A.total_durasi
        FROM ALBUM A
        JOIN LABEL L ON A.id_label = L.id
        WHERE L.email = '{email}';
    """
    data, col = selectQuery(ALBUM_QUERY), ['ID', 'ALBUM_TITLE', 'COUNT_SONG', 'DURATION']

    colnames = col

    results = [dict(zip(colnames, row)) for row in data]

    return results

def getAlbumDetail(album_id):
    ALBUM_DETAIL_QUERY = f"""
        SELECT KONTEN.id, KONTEN.judul AS judul_lagu, KONTEN.durasi AS duration, SONG.total_play, SONG.total_download
        FROM SONG
        INNER JOIN KONTEN ON SONG.id_konten = KONTEN.id
        WHERE SONG.id_album = '{album_id}';
    """
    data, col = selectQuery(ALBUM_DETAIL_QUERY), ['ID', 'SONG_TITLE', 'DURATION', 'TOTAL_PLAY', 'TOTAL_DOWNLOAD']

    colnames = col

    results = [dict(zip(colnames, row)) for row in data]

    print(results)

    return results

