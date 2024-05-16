import psycopg2
import random
from django.shortcuts import render
from pathlib import Path
from django.http import Http404

BASE_DIR = Path(__file__).resolve().parent.parent

def showlistpodcast(request):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres.llzlkweenzlgbpgkbnbd',
        password='marmut13basdatf',
        host='aws-0-ap-southeast-1.pooler.supabase.com',
        port='5432'
    )
    cursor = conn.cursor()

    # Execute a SQL query to fetch podcast data by joining tables
    query = """
        SELECT k.id, k.judul, g.genre 
        FROM marmut.podcast p
        JOIN marmut.konten k ON p.id_konten = k.id
        JOIN marmut.genre g ON p.id_konten = g.id_konten
    """
    cursor.execute(query)
    podcasts = cursor.fetchall()

    # Close the database connection
    conn.close()

    # List of available images
    images = ['pod1.svg', 'pod2.svg', 'pod3.svg']

    # Assign random images to each podcast
    podcast_list = []
    for podcast in podcasts:
        image = random.choice(images)
        podcast_list.append({'id': podcast[0], 'title': podcast[1], 'genre': podcast[2], 'image': image})

    # Pass the fetched data to the template
    return render(request, 'listpodcast.html', {'podcasts': podcast_list})

def showplaypodcast(request, podcast_id):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres.llzlkweenzlgbpgkbnbd',
        password='marmut13basdatf',
        host='aws-0-ap-southeast-1.pooler.supabase.com',
        port='5432'
    )
    cursor = conn.cursor()

    # Fetch podcast details
    query_podcast = """
        SELECT k.judul, g.genre, a.nama, k.durasi, k.tanggal_rilis, EXTRACT(YEAR FROM k.tanggal_rilis)
        FROM marmut.podcast p
        JOIN marmut.konten k ON p.id_konten = k.id
        JOIN marmut.genre g ON p.id_konten = g.id_konten
        JOIN marmut.akun a ON p.email_podcaster = a.email
        WHERE p.id_konten = %s
    """
    cursor.execute(query_podcast, (str(podcast_id),))
    podcast_details = cursor.fetchone()

    if not podcast_details:
        raise Http404("Podcast not found")

    # Fetch podcast episodes
    query_episodes = """
        SELECT e.judul, e.deskripsi, e.durasi, e.tanggal_rilis
        FROM marmut.episode e
        WHERE e.id_konten_podcast = %s
    """
    cursor.execute(query_episodes, (str(podcast_id),))
    episodes = cursor.fetchall()

    # Close the database connection
    conn.close()

    # List of available images
    episode_images = ['cov1.svg', 'cov2.svg', 'cov3.svg']

    # Calculate total duration in hours and minutes
    total_duration_minutes = sum([episode[2] for episode in episodes])
    total_duration_hours, total_duration_minutes = divmod(total_duration_minutes, 60)
    total_duration = f"{total_duration_hours} jam {total_duration_minutes} menit" if total_duration_hours > 0 else f"{total_duration_minutes} menit"

    # Format episode durations and assign random images
    formatted_episodes = []
    for episode in episodes:
        episode_duration_hours, episode_duration_minutes = divmod(episode[2], 60)
        formatted_duration = f"{episode_duration_hours} jam {episode_duration_minutes} menit" if episode_duration_hours > 0 else f"{episode_duration_minutes} menit"
        image = random.choice(episode_images)
        formatted_episodes.append({
            'title': episode[0],
            'description': episode[1],
            'duration': formatted_duration,
            'release_date': episode[3].strftime("%d %B %Y"),  # Format date to a readable format
            'image': image
        })

    # Pass the fetched data to the template
    context = {
        'title': podcast_details[0],
        'genre': podcast_details[1],
        'podcaster': podcast_details[2],
        'total_duration': total_duration,
        'release_date': podcast_details[4].strftime("%d %B %Y"),  # Format date to a readable format
        'year': podcast_details[5],
        'episodes': formatted_episodes
    }
    return render(request, 'playpodcast.html', context)
