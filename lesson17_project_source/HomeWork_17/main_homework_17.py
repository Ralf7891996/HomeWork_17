from flask import request
from flask_restx import Api, Resource

from HomeWork_17.shema import movies_schema, movie_schema, directors_schema, director_schema, genres_schema, genre_schema
from app import app, Movie, db, Director, Genre

api = Api(app)
movies_ns = api.namespace('movies')
director_ns = api.namespace("directors")
genre_ns = api.namespace("genres")


# создаем CBV для обработки GET и POST запросов для сущности Фильмы
@movies_ns.route('/')
class MoviesView(Resource):

    def get(self):

        director_id = request.args.get("director_id")
        genre_id = request.args.get("genre_id")

        if director_id is not None and genre_id is not None:
            movies_filter = Movie.query.filter(Movie.director_id == director_id, Movie.genre_id == genre_id)
            return movies_schema.dump(movies_filter), 200

        if director_id is not None and genre_id is None:
            movies_by_director = Movie.query.filter(Movie.director_id == director_id)
            return movies_schema.dump(movies_by_director), 200

        if genre_id is not None and director_id is None:
            movies_by_genre = Movie.query.filter(Movie.genre_id == genre_id)
            return movies_schema.dump(movies_by_genre), 200

        if genre_id is None and director_id is None:
            all_movies = Movie.query.all()
            return movies_schema.dump(all_movies), 200


    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return "movie_added", 201


# создаем CBV для обработки GET, PUT, PATCH и DELETE запросов для сущности Фильмы
@movies_ns.route("/<int:mid>")
class MovieView(Resource):

    def get(self, mid):
        try:
            movie = Movie.query.get(mid)
            return movie_schema.dump(movie)
        except Exception:
            return "Error 404", 404

    def put(self, mid):
        req_json = request.json
        update_movie = Movie.query.get(mid)
        update_movie.title = req_json.get("title")
        update_movie.description = req_json.get("description")
        update_movie.trailer = req_json.get("trailer")
        update_movie.year = req_json.get("year")
        update_movie.rating = req_json.get("rating")
        update_movie.genre_id = req_json.get("genre_id")
        update_movie.director_id = req_json.get("director_id")

        db.session.add(update_movie)
        db.session.commit()
        return "movie_update", 204

    def patch(self, mid):
        req_json = request.json
        update_movie = Movie.query.get(mid)
        if req_json.get("title") is not None:
            update_movie.title = req_json.get("title")
        if req_json.get("description") is not None:
            update_movie.description = req_json.get("description")
        if req_json.get("trailer") is not None:
            update_movie.trailer = req_json.get("trailer")
        if req_json.get("year") is not None:
            update_movie.year = req_json.get("year")
        if req_json.get("rating") is not None:
            update_movie.rating = req_json.get("rating")
        if req_json.get("genre_id") is not None:
            update_movie.genre_id = req_json.get("genre_id")
        if req_json.get("director_id") is not None:
            update_movie.director_id = req_json.get("director_id")

        db.session.add(update_movie)
        db.session.commit()
        return "movie_update", 204

    def delete(self, mid):
        delete_movie = Movie.query.get(mid)
        db.session.delete(delete_movie)
        db.session.commit()
        return "movie_deleted", 204


# создаем CBV для обработки GET и POST запросов для сущности Режиссеры
@director_ns.route("/")
class DirectorsView(Resource):
    def get(self):
        all_directors = db.session.query(Director)
        return directors_schema.dump(all_directors), 200

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        with db.session.begin():
            db.session.add(new_director)
        return "director_added", 201


# создаем CBV для обработки GET, PUT, PATCH и DELETE запросов для сущности Режессеры
@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did):
        director = Director.query.get(did)
        return director_schema.dump(director), 200

    def put(self, did):
        update_director = Director.query.get(did)
        req_json = request.json
        update_director.name = req_json.get("name")
        db.session.add(update_director)
        db.session.commit()
        return "director_update", 204

    def patch(self, did):
        update_director = Director.query.get(did)
        req_json = request.json
        if req_json.get("name") is not None:
            update_director.name = req_json.get("name")
        db.session.add(update_director)
        db.session.commit()
        return "director_update", 204

    def delete(self, did):
        delete_director = Director.query.get(did)
        db.session.delete(delete_director)
        db.session.commit()
        return "director_deleted", 204


# создаем CBV для обработки GET и POST запросов для сущности Жанры
@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        all_genres = Genre.query.all()
        return genres_schema.dump(all_genres)

    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)
        db.session.add(new_genre)
        db.session.commit()
        return "genre_added", 201


# создаем CBV для обработки GET, PUT, PATCH и DELETE запросов для сущности Жанры
@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid):
        genre = Genre.query.get(gid)
        return genre_schema.dump(genre)

    def put(self, gid):
        update_genre = Genre.query.get(gid)
        req_json = request.json
        update_genre.name = req_json.get(gid)
        db.session.add(update_genre)
        db.session.commit()
        return "genre_update", 204

    def patch(self, gid):
        update_genre = Genre.query.get(gid)
        req_json = request.json
        if req_json.get(gid) is not None:
            update_genre.name = req_json.get(gid)
        db.session.add(update_genre)
        db.session.commit()
        return "genre_update", 204

    def delete(self, gid):
        delete_genre = Genre.query.get(gid)
        db.session.delete(delete_genre)
        db.session.commit()
        return "genre_deleted", 204


if __name__ == '__main__':
    app.run(debug=True)