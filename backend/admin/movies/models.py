from uuid import uuid4

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255, unique=True)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class FilmWorkType(models.TextChoices):
    MOVIE = 'movie', _('Movie')
    TV_SHOW = 'tv_show', _('TV Show')


class FilmWork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('title'), max_length=255)
    description = models.CharField(_('description'), blank=True, max_length=4096)
    creation_date = models.DateField(_('creation_date'), blank=True,)
    file_path = models.CharField(_('file_path'), max_length=4096, blank=True, default='')
    rating = models.FloatField(_('rating'), null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    type = models.CharField(_('type'), choices=FilmWorkType.choices, default=FilmWorkType.MOVIE, max_length=255)

    genres = models.ManyToManyField('Genre', through='GenreFilmWork', related_name='films')
    persons = models.ManyToManyField('Person', through='PersonFilmWork')

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _('Film')
        verbose_name_plural = _('Films')

    def __str__(self):
        return self.title


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE, verbose_name=_('Film Work'))
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, verbose_name=_('Genre'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
        indexes = (models.Index(fields=['film_work', 'genre']),)


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full_name'), max_length=512)

    films = models.ManyToManyField(FilmWork, through='PersonFilmWork')

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'content"."person'
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')


class PersonFilmWorkRole(models.TextChoices):
    ACTOR = 'actor', _('Actor')
    WRITER = 'writer', _('Writer')
    DIRECTOR = 'director', _('Director')


class PersonFilmWork(UUIDMixin):
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE, verbose_name=_('Film Work'))
    person = models.ForeignKey('Person', on_delete=models.CASCADE, verbose_name=_('Person'))
    role = models.CharField(_('role'), choices=PersonFilmWorkRole.choices, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        constraints = (
            models.UniqueConstraint(fields=['film_work', 'person', 'role'], name='person_film_work_unique_idx'),
        )
