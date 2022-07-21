import enum


class NoneEnum(enum.Enum):
    none = None


class StrValueEnum(enum.Enum):
    @classmethod
    def find_element(cls, value: str):

        for elem in cls:
            if elem.value.lower() == value.lower():
                return elem
        return NoneEnum.none


class FilmWorkType(StrValueEnum):
    tv_show = 'tv show'
    movie = 'movie'


class PersonFilmWorkRole(StrValueEnum):
    actor = 'actor'
    director = 'director'
    writer = 'writer'
