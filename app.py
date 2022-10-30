# app.py

from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy

from config import db, app
from models import Movie, Director, Genre
from schemas import MovieSchema, DirectorSchema, GenreSchema

api = Api(app)

# обьекты сериализации/десерализации
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

# создаем неймспейсы
movie_ns = api.namespace('movies')
director_ns = api.namespace('director')
genre_ns = api.namespace('genre')


@movie_ns.route("/")
class MoviesViews(Resource):
    def get(self):
        """Возвращает список всех фильмов"""
        req_genre_id = request.args.get("genre_id")
        req_director_id = request.args.get("director_id")
        if req_genre_id and req_director_id:
            movies = Movie.query.filter(Movie.genre_id == req_genre_id,
                                           Movie.director_id == req_director_id).all()
            return movies_schema.dump(movies), 200

        all_movies = Movie.query.all()
        return movies_schema.dump(all_movies), 200

    def post(self):
        """Добавляем фильм"""
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return "", 201



@movie_ns.route("/<int:id>")
class MovieView(Resource):
    def get(self, id: int):
        """Возвращает фильм по id"""
        try:
            one_movie = Movie.query.filter(Movie.id == id).one()
            return movie_schema.dump(one_movie), 200
        except Exception as error:
            return str(error), 404

    def put(self, id: int):
        """Обновляет фильм"""
        movie = Movie.query.filter(Movie.id == id).one()
        req_json = request.json

        if "title" in req_json:
            movie.title = req_json.get("title")
        if "description" in req_json:
            movie.description = req_json.get("description")
        if "trailer" in req_json:
            movie.trailer = req_json.get("trailer")
        if "year" in req_json:
            movie.year = req_json.get("year")
        if "rating" in req_json:
            movie.rating = req_json.get("rating")
        if "genre_id" in req_json:
            movie.genre_id = req_json.get("genre_id")
        if "director_id" in req_json:
            movie.director_id = req_json.get("director_id")

        db.session.add(movie)
        db.session.commit()
        return "", 204


    def delete(self, id: int):
        """Удаляем фильм"""
        movie = Movie.query.filter(Movie.id == id).one()
        db.session.delete(movie)
        db.session.commit()
        return "", 204


@director_ns.route("/<name>")
class DirectorViews(Resource):
    def post(self, name):
        """Добавляем режиссера"""
        new_director = Director(name=name)
        with db.session.begin():
            db.session.add(new_director)
        return '', 201



@movie_ns.route("/directors/<int:uid>")
class DirectorsViews(Resource):
    def get(self, uid: int):
        """Получаем все фильмы режиссера по его id """
        try:
            movies_by_director = Movie.query.filter(Movie.director_id == uid).all()
            return movies_schema.dump(movies_by_director), 200
        except Exception:
            return "", 404

    def put(self, id: int):
        """Обновляет режжисера"""
        director = Director.query.filter(Director.id == id).one()
        req_json = request.json

        director.name = req_json.get("name")

        db.session.add(director)
        db.session.commit()
        return "", 204

    def delete(self, id: int):
        """Удаляем режжисера"""
        director = Director.query.filter(Director.id == id).one()
        db.session.delete(director)
        db.session.commit()
        return "", 204


@genre_ns.route("/<name>")
class GenreViews(Resource):
    def post(self, name):
        """Добавляем жанр"""
        new_genre = Genre(name=name)
        with db.session.begin():
            db.session.add(new_genre)
        return '', 201


@movie_ns.route("/genres/<int:uid>")
class GenresViews(Resource):
    def get(self, uid: int):
        """Получаем все фильмы одного жанра по его id """
        try:
            movies_by_genres = Movie.query.filter(Movie.genre_id == uid).all()
            return movies_schema.dump(movies_by_genres), 200
        except Exception:
            return "", 404
    def put(self, id: int):
        """Обновляет жанр"""
        try:
            genre = Genre.query.filter(Genre.id == id).one()
            req_json = request.json

            genre.name = req_json.get("name")

            db.session.add(genre)
            db.session.commit()
            return
        except Exception as error:
            return str(error), 404

    def delete(self, id: int):
        """Удаляем жанр"""
        genre = Genre.query.filter(Genre.id == id).one()
        db.session.delete(genre)
        db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run(debug=True)