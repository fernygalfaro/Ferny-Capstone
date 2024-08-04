import requests
import psycopg2
from config import TMDB_API_KEY, DATABASE

# Database connection
connection = psycopg2.connect(**DATABASE)
cursor = connection.cursor()

# Create Tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS genres (
        genre_id SERIAL PRIMARY KEY,
        genre_name VARCHAR(255) NOT NULL
    ); 
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        movie_id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        release_year INT, 
        rating DECIMAL(2, 1)
    ); 
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS movie_genres (
        movie_id INT, 
        genre_id INT, 
        PRIMARY KEY (movie_id, genre_id),
        FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
        FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
    ); 
""")
connection.commit()


def fetch_genres():
    try:
        response = requests.get(f'https://api.themoviedb.org/3/genre/movie/list', params={'api_key': TMDB_API_KEY})
        response.raise_for_status()
        genres = response.json().get('genres', [])
        for genre in genres:
            cursor.execute(
                "INSERT INTO genres (genre_id, genre_name) VALUES (%s, %s) ON CONFLICT (genre_id) DO NOTHING",
                (genre['id'], genre['name']))
        connection.commit()
    except requests.RequestException as e:
        print(f"Error fetching genres: {e}")
    except psycopg2.Error as e:
        print(f"Database error: {e}")


def fetch_movies(page=1):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/popular',
                                params={'api_key': TMDB_API_KEY, 'page': page})
        response.raise_for_status()
        movies = response.json().get('results', [])
        for movie in movies:
            cursor.execute("INSERT INTO movies (title, release_year, rating) VALUES (%s, %s, %s) RETURNING movie_id",
                           (movie['title'], movie['release_date'][:4], movie['vote_average']))
            movie_id = cursor.fetchone()[0]
            for genre_id in movie['genre_ids']:
                cursor.execute("INSERT INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)", (movie_id, genre_id))
        connection.commit()
    except requests.RequestException as e:
        print(f"Error fetching movies: {e}")
    except psycopg2.Error as e:
        print(f"Database error: {e}")


if __name__ == '__main__':
    fetch_genres()  # Fetch and Store Genres
    fetch_movies()  # Fetch and Store Movies

    cursor.close()
    connection.close()
