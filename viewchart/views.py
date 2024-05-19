import psycopg2
import random
from django.shortcuts import render
from datetime import datetime, timedelta

# Create your views here.
def showviewchart(request):
    context = {
        'show_navbar': True,
        'user_role': {
            'label': False,
            'podcast': True,
            'artist': True,
            'songwriter': True
        }
    }
    return render(request, "viewchart.html", context)

def fetch_songs(cursor, limit=20):
    query = """
        SELECT s.id_konten, k.judul, ak.nama, k.tanggal_rilis, s.total_play
        FROM marmut.song s
        JOIN marmut.artist a ON s.id_artist = a.id
        JOIN marmut.akun ak ON a.email_akun = ak.email
        JOIN marmut.konten k ON s.id_konten = k.id
        WHERE s.total_play > 0
        ORDER BY s.total_play DESC
        LIMIT %s
    """
    cursor.execute(query, (limit,))
    return cursor.fetchall()

def showdailypagechart(request):
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres.llzlkweenzlgbpgkbnbd',
        password='marmut13basdatf',
        host='aws-0-ap-southeast-1.pooler.supabase.com',
        port='5432'
    )
    cursor = conn.cursor()

    songs = fetch_songs(cursor)
    conn.close()

    images = ['top1.svg', 'top2.svg', 'top3.svg']
    song_list = []
    for song in songs:
        image = random.choice(images)
        song_list.append({
            'id': song[0],
            'title': song[1],
            'artist': song[2],
            'release_date': song[3].strftime('%d %B %Y'),
            'total_plays': song[4],
            'image': image
        })

    context = {
        'show_navbar': True,
        'songs': song_list
    }
    return render(request, "dailypage.html", context)

def showweeklypagechart(request):
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres.llzlkweenzlgbpgkbnbd',
        password='marmut13basdatf',
        host='aws-0-ap-southeast-1.pooler.supabase.com',
        port='5432'
    )
    cursor = conn.cursor()

    songs = fetch_songs(cursor)
    conn.close()

    images = ['top1.svg', 'top2.svg', 'top3.svg']
    song_list = []
    for song in songs:
        image = random.choice(images)
        song_list.append({
            'id': song[0],
            'title': song[1],
            'artist': song[2],
            'release_date': song[3].strftime('%d %B %Y'),
            'total_plays': song[4],
            'image': image
        })

    context = {
        'show_navbar': True,
        'songs': song_list
    }
    return render(request, "weeklypage.html", context)

def showmonthlypagechart(request):
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres.llzlkweenzlgbpgkbnbd',
        password='marmut13basdatf',
        host='aws-0-ap-southeast-1.pooler.supabase.com',
        port='5432'
    )
    cursor = conn.cursor()

    songs = fetch_songs(cursor)
    conn.close()

    images = ['top1.svg', 'top2.svg', 'top3.svg']
    song_list = []
    for song in songs:
        image = random.choice(images)
        song_list.append({
            'id': song[0],
            'title': song[1],
            'artist': song[2],
            'release_date': song[3].strftime('%d %B %Y'),
            'total_plays': song[4],
            'image': image
        })

    context = {
        'show_navbar': True,
        'songs': song_list
    }
    return render(request, "monthlypage.html", context)

def showyearlypagechart(request):
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres.llzlkweenzlgbpgkbnbd',
        password='marmut13basdatf',
        host='aws-0-ap-southeast-1.pooler.supabase.com',
        port='5432'
    )
    cursor = conn.cursor()

    songs = fetch_songs(cursor)
    conn.close()

    images = ['top1.svg', 'top2.svg', 'top3.svg']
    song_list = []
    for song in songs:
        image = random.choice(images)
        song_list.append({
            'id': song[0],
            'title': song[1],
            'artist': song[2],
            'release_date': song[3].strftime('%d %B %Y'),
            'total_plays': song[4],
            'image': image
        })

    context = {
        'show_navbar': True,
        'songs': song_list
    }
    return render(request, "yearlypage.html", context)
