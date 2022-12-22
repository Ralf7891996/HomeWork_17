
# Пишем схемы для моделей Movie, Director, Genre

from marshmallow import Schema, fields


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()


class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


directors_schema = DirectorSchema(many=True)
director_schema = DirectorSchema()


class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()