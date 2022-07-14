from movies.models import FilmWork, PersonFilmWorkRole
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class MovieSerializer(ModelSerializer):
    genres = SerializerMethodField('get_genres_name')
    directors = SerializerMethodField('get_directors')
    actors = SerializerMethodField('get_actors')
    writers = SerializerMethodField('get_writers')

    class Meta:
        model = FilmWork
        fields = (
            'id',
            'title',
            'description',
            'creation_date',
            'file_path',
            'rating',
            'type',
            'genres',
            'directors',
            'actors',
            'writers',
        )

    def get_genres_name(self, film_work: FilmWork):
        return (genre.name for genre in film_work._genres)

    def get_directors(self, film_work: FilmWork):
        return set(person.full_name for person in film_work._persons if person.role == PersonFilmWorkRole.DIRECTOR)

    def get_actors(self, film_work: FilmWork):
        return set(person.full_name for person in film_work._persons if person.role == PersonFilmWorkRole.ACTOR)

    def get_writers(self, film_work: FilmWork):
        return set(person.full_name for person in film_work._persons if person.role == PersonFilmWorkRole.WRITER)
