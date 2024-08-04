from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import mongo
import os
from werkzeug.utils import secure_filename

profile = Blueprint('profile', __name__)

@profile.route('/complete_profile', methods=['GET', 'POST'])
def complete_profile():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        birthday = request.form.get('birthday')
        favorite_movies = request.form.get('favorite_movies').split(',')
        profile_picture = request.files['profile_picture']

        # Save the profile picture
        if profile_picture:
            filename = secure_filename(profile_picture.filename)
            profile_picture.save(os.path.join('app/static/Pictures', filename))
            picture_path = f'Pictures/{filename}'
        else:
            picture_path = 'Pictures/default.jpg'  # Default picture if none uploaded

        mongo.db.users.update_one(
            {'email': email},  # Assuming email is unique and passed in hidden field
            {'$set': {
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'birthday': birthday,
                'favorite_movies': favorite_movies,
                'profile_picture': picture_path
            }}
        )
        flash('Profile completed successfully!', 'success')
        return redirect(url_for('main.home'))

    return render_template('complete_profile.html')
