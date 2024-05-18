import uuid
from django.db import connection
from django.shortcuts import redirect, render
from Authentication.views import selectQuery, modifyQuery, get_user_data

# Fungsi Views untuk menampilkan Album ROLE -> LABEL
def showAlbumLabel(request):
    email = request.COOKIES.get('login')
    context = get_user_data(email)
    context['albums'] = getAlbumLabel(email)
    return render(request, "manageAlbumLabel.html", context)

# Fungsi Views untuk menampilkan Album ROLE -> ARTIST/SONGWRITER
def showAlbum(request):
    email = request.COOKIES.get('login')
    context = get_user_data(email)
    context['albums'] = getAlbums(email)
    context['labels'] = getLabel()
    if(context['user_role']['artist'] == False):
        context['artists'] = getArtist()
    context['songwriters'] = getSongWriter()
    context['genres'] = getGenre()
    return render(request, "manageAlbum.html", context)

# Fungsi Views untuk menampilkan lagu pada album ROLE -> LABEL
def showSongLabel(request, album_id):
    email = request.COOKIES.get('login')
    context = get_user_data(email)
    context['songs'] = getAlbumDetail(album_id)
    context['album'] = getAlbum(album_id)
    return render(request, "manageSongLabel.html", context)

# Fungsi Views untuk menampilkan Lagu pada Album ROLE -> ARTIST, SONGWRITER
def showSong(request, album_id):
    email = request.COOKIES.get('login')
    context = get_user_data(email)
    context['album'] = getAlbum(album_id)
    if(context['user_role']['artist'] == False):
        context['artists'] = getArtist()
    context['songwriters'] = getSongWriter()
    context['genres'] = getGenre()
    context['songs'] = getAlbumDetail(album_id)
    return render(request, "manageSong.html", context)

# Fungsi untuk mengecek Royalty pada ROLE -> ARTIST, SONGWRITER, LABEL
def showRoyaltyCheck(request):
    email = request.COOKIES.get('login')
    context = get_user_data(email)
    context['royaltyData'] = getRoyalty(email)
    return render(request, "royaltyCheck.html", context)

# Fungsi bantuan untuk menambahkan Album 
def addAlbum(request):
    email = request.COOKIES.get('login')
    context = get_user_data(email)
    context['albums'] = getAlbums(email)
    context['labels'] = getLabel()
    context['artists'] = getArtist()
    context['songwriters'] = getSongWriter()
    context['genres'] = getGenre()
    if request.method  == 'POST':
        ARTIST_QUERY = f"""
            SELECT id FROM ARTIST
            JOIN AKUN AS A ON A.email = email_akun
            WHERE A.nama = '{request.POST.get('artist')}'
        """

        ARTISTS_QUERY = f"""
            SELECT id FROM ARTIST
            JOIN AKUN AS A ON A.email = email_akun
            WHERE A.nama = '{request.POST.get('artists')}'
        """

        artist= ''
        title = request.POST.get('title')
        label = request.POST.get('label')
        song_title = request.POST.get('song_title')
        if(context['user_role']['artist'] == True):
            artist = selectQuery(ARTIST_QUERY)[0][0]
        else:
            artist = selectQuery(ARTISTS_QUERY)[0][0]
        songwriters = request.POST.getlist('songwriters[]')
        genres = request.POST.getlist('genres[]')
        duration = request.POST.get('durasi')
        album_id = str(uuid.uuid4())
        song_id = str(uuid.uuid4())        

        INSERT_ALBUM_QUERY = f"""
            INSERT INTO ALBUM VALUES ('{album_id}', '{title}', 0, '{label}', 0);
        """

        INSERT_SONG_QUERY = f"""
            INSERT INTO SONG VALUES ('{song_id}', '{artist}', '{album_id}', 0, 0);
        """

        INSERT_KONTEN_QUERY = f"""
        INSERT INTO KONTEN VALUES ('{song_id}', '{song_title}', CURRENT_DATE, EXTRACT(YEAR FROM CURRENT_DATE), {duration});
        """

        INSERT_SONGWRITER_QUERIES = [ f"""
            INSERT INTO SONGWRITER_WRITE_SONG VALUES ('{songwriter_id}', '{song_id}');
         """ for songwriter_id in songwriters]

        INSERT_GENRE_QUERIES = [ f"""
            INSERT INTO GENRE VALUES ('{song_id}', '{genre}');
        """ for genre in genres]

        modifyQuery(INSERT_ALBUM_QUERY)        
        modifyQuery(INSERT_KONTEN_QUERY)   
        modifyQuery(INSERT_SONG_QUERY)     

        for INSERT_QUERY in INSERT_SONGWRITER_QUERIES:
            modifyQuery(INSERT_QUERY)  

        for INSERT_QUERY in INSERT_GENRE_QUERIES:
            modifyQuery(INSERT_QUERY)

    return redirect('SongAlbum:show_album')

def addSong(request, album_id):
    email = request.COOKIES.get('login')
    context = get_user_data(email)
    if request.method  == 'POST':
        ARTIST_QUERY = f"""
            SELECT id FROM ARTIST
            JOIN AKUN AS A ON A.email = email_akun
            WHERE A.nama = '{request.POST.get('artist')}'
        """

        ARTISTS_QUERY = f"""
            SELECT id FROM ARTIST
            JOIN AKUN AS A ON A.email = email_akun
            WHERE A.nama = '{request.POST.get('artists')}'
        """

        artist= ''
        song_title = request.POST.get('song_title')
        if(context['user_role']['artist'] == True):
            artist = selectQuery(ARTIST_QUERY)[0][0]
        else:
            artist = selectQuery(ARTISTS_QUERY)[0][0]
        songwriters = request.POST.getlist('songwriters[]')
        genres = request.POST.getlist('genres[]')
        duration = request.POST.get('durasi')
        song_id = str(uuid.uuid4())

        INSERT_SONG_QUERY = f"""
            INSERT INTO SONG VALUES ('{song_id}', '{artist}', '{album_id}', 0, 0);
        """

        INSERT_KONTEN_QUERY = f"""
        INSERT INTO KONTEN VALUES ('{song_id}', '{song_title}', CURRENT_DATE, EXTRACT(YEAR FROM CURRENT_DATE), {duration});
        """

        INSERT_SONGWRITER_QUERIES = [ f"""
            INSERT INTO SONGWRITER_WRITE_SONG VALUES ('{songwriter_id}', '{song_id}');
         """ for songwriter_id in songwriters]

        INSERT_GENRE_QUERIES = [ f"""
            INSERT INTO GENRE VALUES ('{song_id}', '{genre}');
        """ for genre in genres]

        modifyQuery(INSERT_KONTEN_QUERY)   
        modifyQuery(INSERT_SONG_QUERY)     

        for INSERT_QUERY in INSERT_SONGWRITER_QUERIES:
            modifyQuery(INSERT_QUERY)  

        for INSERT_QUERY in INSERT_GENRE_QUERIES:
            modifyQuery(INSERT_QUERY)

    return redirect('SongAlbum:show_song', album_id)

def deleteSong(request, song_id, album_id):
    DELETE_QUERY = f"""
        DELETE FROM PLAYLIST_SONG WHERE id_song='{song_id}';
        DELETE FROM AKUN_PLAY_SONG WHERE id_song='{song_id}';
        DELETE FROM DOWNLOADED_SONG WHERE id_song='{song_id}';
        DELETE FROM SONGWRITER_WRITE_SONG WHERE id_song='{song_id}';
        DELETE FROM ROYALTI WHERE id_song='{song_id}';
        DELETE FROM SONG WHERE id_konten='{song_id}'; 
        DELETE FROM GENRE WHERE id_konten='{song_id}'; 
        DELETE FROM KONTEN WHERE id='{song_id}';
    """

    modifyQuery(DELETE_QUERY)

    return redirect('SongAlbum:show_song', album_id)

def deleteSongLabel(request, song_id, album_id):
    DELETE_QUERY = f"""
        DELETE FROM PLAYLIST_SONG WHERE id_song='{song_id}';
        DELETE FROM AKUN_PLAY_SONG WHERE id_song='{song_id}';
        DELETE FROM DOWNLOADED_SONG WHERE id_song='{song_id}';
        DELETE FROM SONGWRITER_WRITE_SONG WHERE id_song='{song_id}';
        DELETE FROM ROYALTI WHERE id_song='{song_id}';
        DELETE FROM SONG WHERE id_konten='{song_id}';
        DELETE FROM GENRE WHERE id_konten='{song_id}';
        DELETE FROM KONTEN WHERE id='{song_id}';
    """

    modifyQuery(DELETE_QUERY)

    return redirect('SongAlbum:show_song_label', album_id)

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

def getAlbum(album_id):
    ALBUM_QUERY = f"""
        SELECT * FROM ALBUM
        WHERE id='{album_id}';
    """
    data, col = selectQuery(ALBUM_QUERY), ['ID', 'ALBUM_TITLE', 'COUNT_SONG', 'LABEL_ID', 'DURATION']

    colnames = col

    results = [dict(zip(colnames, row)) for row in data]

    return results

def deleteAlbum(request, album_id):
    DELETE_QUERY = f"""
        DELETE FROM PLAYLIST_SONG
        WHERE id_song IN (SELECT id_konten FROM song WHERE id_album='{album_id}');
        DELETE FROM AKUN_PLAY_SONG
        WHERE id_song IN (SELECT id_konten FROM song WHERE id_album='{album_id}');
        DELETE FROM DOWNLOADED_SONG 
        WHERE id_song IN (SELECT id_konten FROM song WHERE id_album='{album_id}');
        DELETE FROM SONGWRITER_WRITE_SONG
        WHERE id_song IN (SELECT id_konten FROM song WHERE id_album='{album_id}');
        DELETE FROM ROYALTI
        WHERE id_song IN (SELECT id_konten FROM song WHERE id_album='{album_id}');
        DELETE FROM GENRE
        WHERE id_konten IN (SELECT id_konten FROM song WHERE id_album='{album_id}');
        DELETE FROM SONG WHERE id_album='{album_id}';
        DELETE FROM KONTEN
        WHERE id NOT IN (SELECT id_konten FROM SONG UNION SELECT id_konten FROM PODCAST);
        DELETE FROM ALBUM WHERE id='{album_id}';
    """

    modifyQuery(DELETE_QUERY)

    return redirect('SongAlbum:show_album')

def deleteAlbumLabel(request, album_id):
    DELETE_QUERY = f"""
        DELETE FROM PLAYLIST_SONG
        WHERE id_song IN (SELECT id_konten FROM song WHERE id_album='{album_id}');
        DELETE FROM AKUN_PLAY_SONG
        WHERE id_song IN (SELECT id_konten FROM song WHERE id_album='{album_id}');
        DELETE FROM DOWNLOADED_SONG 
        WHERE id_song IN (SELECT id_konten FROM song WHERE id_album='{album_id}');
        DELETE FROM SONGWRITER_WRITE_SONG
        WHERE id_song IN (SELECT id_konten FROM song WHERE id_album='{album_id}');
        DELETE FROM ROYALTI
        WHERE id_song IN (SELECT id_konten FROM song WHERE id_album='{album_id}');
        DELETE FROM GENRE
        WHERE id_konten IN (SELECT id_konten FROM song WHERE id_album='{album_id}');
        DELETE FROM SONG WHERE id_album='{album_id}';
        DELETE FROM KONTEN
        WHERE id NOT IN (SELECT id_konten FROM SONG UNION SELECT id_konten FROM PODCAST);
        DELETE FROM ALBUM WHERE id='{album_id}';
    """

    modifyQuery(DELETE_QUERY)

    return redirect('SongAlbum:show_album_label')

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

def getLabel():
    LABEL_QUERY = f"""
        SELECT id, nama FROM LABEL
    """
    data, col = selectQuery(LABEL_QUERY), ['ID', 'LABEL_NAME']

    colnames = col

    results = [dict(zip(colnames, row)) for row in data]

    print(results)

    return results

def getArtist():
    ARTIST_QUERY = f"""
        SELECT ARTIST.id, AKUN.nama FROM ARTIST
        JOIN AKUN ON ARTIST.email_akun = AKUN.email
    """
    data, col = selectQuery(ARTIST_QUERY), ['ID', 'ARTIST_NAME']

    colnames = col

    results = [dict(zip(colnames, row)) for row in data]

    print(results)

    return results

def getSongWriter():
    SONGWRITER_QUERY = f"""
        SELECT id, nama FROM SONGWRITER
        JOIN AKUN ON AKUN.email = SONGWRITER.email_akun
    """
    data, col = selectQuery(SONGWRITER_QUERY), ['ID', 'SONGWRITER_NAME']

    colnames = col

    results = [dict(zip(colnames, row)) for row in data]

    print(results)

    return results

def getGenre():
    SONGWRITER_QUERY = f"""
        SELECT DISTINCT genre FROM GENRE
    """
    data, col = selectQuery(SONGWRITER_QUERY), ['GENRE']

    colnames = col

    results = [dict(zip(colnames, row)) for row in data]

    print(results)

    return results