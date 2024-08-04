# app/routes.py
import random
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

@main.route('/')
def home():
    movies = list(current_app.db.movies.find())
    movie_count = len(movies)
    if movie_count > 0:
        random_index = random.randint(0, movie_count - 1)
        random_movie = movies[random_index]
        movie_info = {
            'backdrop_url': random_movie.get('backdrop_url'),
            'overview': random_movie.get('overview'),
            'release_date': random_movie.get('release_date'),
            'title': random_movie.get('title'),
            'poster_url': random_movie.get('poster_url'),
        }
        return render_template('SoundScene.html', movie=movie_info)
    else:
        return render_template('SoundScene.html', movie=None)

@main.route('/discover/movies')
def discover_movies():
    movies = current_app.db.movies.find()
    return render_template('DiscoverMovies.html', movies=movies)

@main.route('/discover/music')
def discover_music():
    music = current_app.db.music.find()
    return render_template('DiscoverMusic.html', music=music)

@main.route('/discover/community_music')
def discover_community_music():
    return render_template('DiscoverCommunityMusic.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = current_app.db.users.find_one({'email': email})

        if user and check_password_hash(user['password'], password):
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        if current_app.db.users.find_one({'email': email}):
            flash('Email address already exists', 'danger')
        else:
            current_app.db.users.insert_one({
                'email': email,
                'password': hashed_password
            })
            flash('Registration successful!', 'success')
            return redirect(url_for('main.login'))

    return render_template('register.html')

@main.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birthday = request.form['birthday']
        favorite_movie = request.form['favorite_movie']
        favorite_band = request.form['favorite_band']
        picture = request.form['picture']

        current_app.db.users.update_one(
            {'email': email},
            {'$set': {
                'first_name': first_name,
                'last_name': last_name,
                'birthday': birthday,
                'favorite_movie': favorite_movie,
                'favorite_band': favorite_band,
                'picture': picture
            }}
        )
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.home'))

    return render_template('profile.html')

@main.route('/about')
def about():
    return render_template('About.html')

@main.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('query', '').lower()
    movies = current_app.db.movies.find({"title": {"$regex": query, "$options": "i"}})
    return render_template('SearchResults.html', query=query, movies=movies)
