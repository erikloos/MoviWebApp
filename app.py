"""Handles the MoviWebApp logic."""

import os
from flask import Flask, redirect, render_template, request, Response

from movie_api import get_search_api_response, validate_and_parse_api_response
from data_manager import DataManager
from models import db

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data_manager = DataManager()


@app.route('/')
def index() -> str:
    """Display all movies from the database (all users) on the home page."""
    movies = data_manager.get_all_movies()
    return render_template('index.html', movies=movies)


@app.route('/users', methods=['GET'])
def list_users() -> str:
    """Display all users."""
    users = data_manager.get_users()
    return render_template('users.html', users=users)


@app.route('/users', methods=['POST'])
def create_user() -> Response:
    """Create a new user in the database and redirect to the homepage."""
    user_name = request.form.get('name')
    user_id = data_manager.create_user(user_name)
    return redirect(f'/users/{user_id}/movies')


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def list_movies(user_id: int) -> str:
    """Display all movies of a specific user."""
    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movies=movies, user_id=user_id)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id: int) -> str | Response:
    """Search for a movie via OMDB API and add it to the user's database."""
    search_title = request.form.get('title')
    response = get_search_api_response(search_title)
    if response is None:
        movies = data_manager.get_movies(user_id)
        return render_template('movies.html',
                               movies=movies,
                               user_id=user_id,
                               error="API not reachable! Try again later")

    movie_info = response.json()

    movie_data = validate_and_parse_api_response(movie_info)
    if movie_data is None:
        movies = data_manager.get_movies(user_id)
        return render_template('movies.html',
                               movies=movies,
                               user_id=user_id,
                               error="Movie could not be found!")
    data_manager.add_movies(movie_data, user_id)

    return redirect(f'/users/{user_id}/movies')


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id: int, movie_id: int) -> Response:
    """Update the movie title of a specific movie."""
    new_title = request.form.get("new_title")
    data_manager.update_movie(movie_id, new_title)

    return redirect(f'/users/{user_id}/movies')


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id: int, movie_id: int) -> Response:
    """Delete a movie from the user's database."""
    data_manager.delete_movie(movie_id)
    return redirect(f'/users/{user_id}/movies')


@app.errorhandler(404)
def page_not_found(e) -> tuple:
    """Handle the 404 error and display an error page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(port=5002)
