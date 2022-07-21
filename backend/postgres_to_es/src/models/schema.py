import enum

SCHEMA = 'content'


class PersonFilmWorkRoleEnum(str, enum.Enum):
    ACTOR = 'actor'
    WRITER = 'writer'
    DIRECTOR = 'director'


class Schema:
    film_work = 'film_work'
    genre = 'genre'
    person = 'person'
    genre_film_work = 'genre_film_work'
    person_film_work = 'person_film_work'
