from django.db.models import F, Prefetch
from django.db.models.query import QuerySet
from movies.models import FilmWork, Genre, Person
from movies.serializers import MovieSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet


class MoviesApi(ReadOnlyModelViewSet):
    serializer_class = MovieSerializer

    def get_queryset(self) -> QuerySet:
        genre_prefetch = Prefetch('genres', to_attr='_genres', queryset=(Genre.objects.all()))

        person_prefetch = Prefetch(
            'persons', to_attr='_persons', queryset=(Person.objects.all().annotate(role=F('personfilmwork__role'),))
        )

        return FilmWork.objects.prefetch_related(genre_prefetch, person_prefetch)
