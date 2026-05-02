import os
from flask import Flask, redirect, render_template, request

from movie_api import get_search_api_response, validate_and_parse_api_response
from data_manager import DataManager
from models import db

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app. This is the reason you need to import db from models

data_manager = DataManager() # Create an object of your DataManager class

@app.route('/')
def index():
    movies = data_manager.get_all_movies()
    return render_template('index.html', movies=movies)


@app.route('/users', methods=['GET'])
def list_users():
    users = data_manager.get_users()
    return render_template('users.html', users=users)


@app.route('/users', methods=['POST'])
def create_user():
    user_name = request.form.get('name')
    data_manager.create_user(user_name)
    return redirect('/')


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def list_movies(user_id):
    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movies=movies, user_id=user_id)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
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
def update_movie(user_id, movie_id):
    new_title = request.form.get("new_title")
    data_manager.update_movie(movie_id, new_title)

    return redirect(f'/users/{user_id}/movies')


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    return redirect(f'/users/{user_id}/movies')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
  with app.app_context():
    db.create_all()

  app.run(debug=True, port=5002)
