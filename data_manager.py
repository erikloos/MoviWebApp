from models import db, User, Movie

class DataManager():
    # Define Crud operations as methods
    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()


    def get_users(self):
        user_list = []
        users = db.session.query(User).all()
        for user in users:
            user_list.append(user)
        return user_list


    def get_movies(self, user_id):
        movie_list = []
        movies = db.session.query(Movie)\
                  .filter(Movie.user_id == user_id)\
                  .all()
        for movie in movies:
            movie_list.append(movie)
        return movie_list


    def add_movies(self, movie, user_id):
        new_movie = Movie(
            title = movie['title'],
            director = movie['director'],
            publication_year = movie['year'],
            poster_url = movie['poster_url'],
            user_id = user_id
        )
        db.session.add(new_movie)
        db.session.commit()


    def update_movie(self, movie_id, new_title):
        movie = db.session.query(Movie)\
                    .filter(Movie.id == movie_id)\
                    .first()
        if movie is None:
            return
        movie.title = new_title
        db.session.commit()


    def delete_movie(self, movie_id):
        db.session.query(Movie)\
            .filter(Movie.id == movie_id)\
            .delete()
        db.session.commit()

    def get_all_movies(self):
        return db.session.query(Movie).all()