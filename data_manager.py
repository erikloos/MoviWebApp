"""Defines the DataManager class for MoviWebApp"""

from models import db, User, Movie

class DataManager:
    """Manage all database operations."""

    def create_user(self, name: str) -> int:
        """Create a new user in the database and return the user id."""
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user.id


    def get_users(self) -> list[User]:
        """Return all user's in the database."""
        return db.session.query(User).all()


    def get_movies(self, user_id: int) -> list[Movie]:
        """Return all movies of a specific user."""
        return db.session.query(Movie)\
                .filter(Movie.user_id == user_id)\
                .all()


    def add_movies(self, movie: dict, user_id: int) -> None:
        """Add a specific movie to the database for a specific user."""
        new_movie = Movie(
            title = movie['title'],
            director = movie['director'],
            publication_year = movie['year'],
            poster_url = movie['poster_url'],
            user_id = user_id
        )
        db.session.add(new_movie)
        db.session.commit()


    def update_movie(self, movie_id: int, new_title: str) -> None:
        """Changes the movie title for specific movie in the database."""
        movie = db.session.query(Movie)\
                    .filter(Movie.id == movie_id)\
                    .first()
        if movie is None:
            return
        movie.title = new_title
        db.session.commit()


    def delete_movie(self, movie_id: int) -> None:
        """Delete a specific Movie from the database."""
        db.session.query(Movie)\
            .filter(Movie.id == movie_id)\
            .delete()
        db.session.commit()


    def get_all_movies(self) -> list[Movie]:
        """Return a list of all movies from the database"""
        return db.session.query(Movie).all()
