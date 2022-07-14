from django.contrib import admin
from django.db.models import F, Prefetch
from django.utils.translation import gettext_lazy as _

from .models import (FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork,
                     PersonFilmWorkRole)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'get_count_films')
    search_fields = ('name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        film_prefetch = Prefetch('films', to_attr='_films', queryset=(FilmWork.objects.all()))

        return queryset.prefetch_related(film_prefetch)

    @admin.display(description=_('Count films'))
    def get_count_films(self, genre: Genre):
        return len(genre._films)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('full_name',)
    list_display = (
        'full_name',
        'get_director_films',
        'get_actor_films',
        'get_writer_films',
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        film_prefetch = Prefetch(
            'films', to_attr='_films', queryset=(FilmWork.objects.annotate(role=F('personfilmwork__role'),))
        )

        return queryset.prefetch_related(film_prefetch)

    @admin.display(description=_('Film director'))
    def get_director_films(self, person: FilmWork):
        return ', '.join(set(film.title for film in person._films if film.role == PersonFilmWorkRole.DIRECTOR))

    @admin.display(description=_('Film actor'))
    def get_actor_films(self, person: FilmWork):
        return ', '.join(set(film.title for film in person._films if film.role == PersonFilmWorkRole.ACTOR))

    @admin.display(description=_('Film writer'))
    def get_writer_films(self, person: FilmWork):
        return ', '.join(set(film.title for film in person._films if film.role == PersonFilmWorkRole.WRITER))


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'get_genres',
        'get_directors',
        'get_actors',
        'get_writers',
        'creation_date',
        'type',
        'rating',
    )
    list_filter = (
        'type',
        'creation_date',
        'genres__name',
    )
    search_fields = ('title', 'description', 'genres__name')
    autocomplete_fields = (
        'genres',
        'persons',
    )
    inlines = (
        GenreFilmWorkInline,
        PersonFilmWorkInline,
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        genre_prefetch = Prefetch('genres', to_attr='_genres', queryset=(Genre.objects.all()))

        person_prefetch = Prefetch(
            'persons', to_attr='_persons', queryset=(Person.objects.all().annotate(role=F('personfilmwork__role'),))
        )

        return queryset.prefetch_related(genre_prefetch, person_prefetch)

    @admin.display(description=_('Genres'))
    def get_genres(self, film_work: FilmWork):
        return ', '.join((genre.name for genre in film_work._genres))

    @admin.display(description=_('Directors'))
    def get_directors(self, film_work: FilmWork):
        return ', '.join(
            set(person.full_name for person in film_work._persons if person.role == PersonFilmWorkRole.DIRECTOR)
        )

    @admin.display(description=_('Actors'))
    def get_actors(self, film_work: FilmWork):
        return ', '.join(
            set(person.full_name for person in film_work._persons if person.role == PersonFilmWorkRole.ACTOR)
        )

    @admin.display(description=_('Writers'))
    def get_writers(self, film_work: FilmWork):
        return ', '.join(
            set(person.full_name for person in film_work._persons if person.role == PersonFilmWorkRole.WRITER)
        )
