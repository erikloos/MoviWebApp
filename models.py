from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)


class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    director = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


user_movies = db.Table('user_movies',
        db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
        db.Column("movie_id", db.Integer, db.ForeignKey("movies.id"))
                       )

