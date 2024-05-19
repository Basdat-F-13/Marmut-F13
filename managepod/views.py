import uuid
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import psycopg2
from datetime import datetime
import random
from Authentication.views import get_user_data

def connect_db():
    return psycopg2.connect(
        dbname='postgres',
        user='postgres.llzlkweenzlgbpgkbnbd',
        password='marmut13basdatf',
        host='aws-0-ap-southeast-1.pooler.supabase.com',
        port='5432'
    )

def showmanagepod(request):
    email = request.COOKIES.get("login")  # Get the logged-in user's email
    if not email:
        return redirect('login')  # Redirect to login if no email found in cookies

    user = get_user_data(email)
    context = user
    context["show_navbar"] = True

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id_konten, k.judul, g.genre 
        FROM marmut.podcast p
        JOIN marmut.konten k ON p.id_konten = k.id
        JOIN marmut.genre g ON p.id_konten = g.id_konten
        WHERE p.email_podcaster = %s
    """, [email])
    podcasts = cursor.fetchall()
    conn.close()

    if not podcasts:
        message = "Belum Memiliki Podcast"
    else:
        message = None

    # Assign random images to each podcast
    images = ['pod1.svg', 'pod2.svg']
    podcasts_with_images = [(podcast[0], podcast[1], podcast[2], random.choice(images)) for podcast in podcasts]

    context.update({
        'podcasts': podcasts_with_images,
        'message': message
    })

    return render(request, "managepod.html", context)


def showlist(request, podcast_id):
    email = request.COOKIES.get("login")  # Get the logged-in user's email
    if not email:
        return redirect('login')  # Redirect to login if no email found in cookies

    user = get_user_data(email)
    context = user
    context["show_navbar"] = True

    conn = connect_db()
    cursor = conn.cursor()
    
    # Fetch podcast name
    cursor.execute("""
        SELECT k.judul
        FROM marmut.konten k
        JOIN marmut.podcast p ON k.id = p.id_konten
        WHERE p.id_konten = %s
    """, [podcast_id])
    podcast_name = cursor.fetchone()[0]
    
    # Fetch episodes
    cursor.execute("""
        SELECT e.id_episode, e.judul, e.deskripsi, e.durasi, e.tanggal_rilis 
        FROM marmut.episode e
        WHERE e.id_konten_podcast = %s
    """, [podcast_id])
    episodes = cursor.fetchall()
    conn.close()

    # List of available images
    images = ['eps1.svg', 'eps2.svg', 'eps3.svg']

    # Assign random images to each episode
    episode_list = []
    for episode in episodes:
        image = random.choice(images)
        episode_list.append({
            'id': episode[0],
            'title': episode[1],
            'description': episode[2],
            'duration': episode[3],
            'release_date': episode[4].strftime('%d %B %Y'),  # Format the date
            'image': image
        })

    context.update({
        'episodes': episode_list,
        'podcast_id': podcast_id,
        'podcast_name': podcast_name
    })

    return render(request, "list.html", context)

@csrf_exempt
def showcreatepod(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        genre = request.POST.get('genre')
        email_podcaster = request.COOKIES.get("login")  # Get the logged-in user's email

        # Generate a new UUID for the konten id
        konten_id = str(uuid.uuid4())

        # Set the year value based on the current date
        current_year = datetime.now().year

        # Set a default duration value
        default_duration = 0

        conn = connect_db()
        cursor = conn.cursor()
        
        # Insert into the konten table with the generated UUID, current year, and default duration
        cursor.execute("""
            INSERT INTO marmut.konten (id, judul, tanggal_rilis, tahun, durasi) 
            VALUES (%s, %s, NOW(), %s, %s)
        """, [konten_id, title, current_year, default_duration])
        
        # Insert into the genre table
        cursor.execute("""
            INSERT INTO marmut.genre (id_konten, genre) 
            VALUES (%s, %s)
        """, [konten_id, genre])
        
        # Insert into the podcast table
        cursor.execute("""
            INSERT INTO marmut.podcast (id_konten, email_podcaster) 
            VALUES (%s, %s)
        """, [konten_id, email_podcaster])
        
        conn.commit()
        conn.close()
        
        return redirect('managepod:managepod')

    return render(request, "createpod.html")

@csrf_exempt
def showaddepisode(request, podcast_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch podcast name
    cursor.execute("""
        SELECT k.judul
        FROM marmut.konten k
        JOIN marmut.podcast p ON k.id = p.id_konten
        WHERE p.id_konten = %s
    """, [podcast_id])
    podcast_name = cursor.fetchone()[0]

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        duration = request.POST.get('duration')

        # Generate a new UUID for the episode id
        episode_id = str(uuid.uuid4())

        cursor.execute("SET search_path TO marmut;")  # Set the correct schema

        # Disable triggers temporarily
        cursor.execute("SET session_replication_role = 'replica';")

        try:
            # Insert into the episode table
            cursor.execute("""
                INSERT INTO episode (id_episode, id_konten_podcast, judul, deskripsi, durasi, tanggal_rilis) 
                VALUES (%s, %s, %s, %s, %s, NOW())
            """, [episode_id, podcast_id, title, description, duration])

            # Re-enable triggers
            cursor.execute("SET session_replication_role = 'origin';")

            # Update the duration in the konten table
            cursor.execute("""
                UPDATE konten
                SET durasi = durasi + %s
                WHERE id = %s
            """, [duration, podcast_id])

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

        return redirect('managepod:list', podcast_id=podcast_id)

    conn.close()
    return render(request, "addepisode.html", {'podcast_id': podcast_id, 'podcast_name': podcast_name})


@csrf_exempt
def delete_podcast(request, podcast_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SET search_path TO marmut;")  # Set the correct schema

    # Disable triggers temporarily
    cursor.execute("SET session_replication_role = 'replica';")

    try:
        # Fetch and delete all episodes associated with the podcast
        cursor.execute("SELECT id_episode FROM episode WHERE id_konten_podcast = %s", [podcast_id])
        episodes = cursor.fetchall()

        for episode in episodes:
            cursor.execute("DELETE FROM episode WHERE id_episode = %s", [episode[0]])

        # Delete the podcast
        cursor.execute("DELETE FROM podcast WHERE id_konten = %s", [podcast_id])

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        # Re-enable triggers
        cursor.execute("SET session_replication_role = 'origin';")
        conn.close()

    return redirect('managepod:managepod')


@csrf_exempt
def delete_episode(request, episode_id, podcast_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SET search_path TO marmut;")  # Set the correct schema

    # Disable triggers temporarily
    cursor.execute("SET session_replication_role = 'replica';")

    try:
        # Fetch the duration of the episode to be deleted
        cursor.execute("SELECT durasi FROM episode WHERE id_episode = %s", [episode_id])
        duration = cursor.fetchone()[0]

        # Delete the episode
        cursor.execute("DELETE FROM episode WHERE id_episode = %s", [episode_id])

        # Re-enable triggers
        cursor.execute("SET session_replication_role = 'origin';")

        # Update the duration in the konten table
        cursor.execute("""
            UPDATE konten
            SET durasi = durasi - %s
            WHERE id = %s
        """, [duration, podcast_id])

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

    return redirect('managepod:list', podcast_id=podcast_id)
