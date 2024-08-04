# app/login.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
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

@auth.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/profile', methods=['GET', 'POST'])
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
