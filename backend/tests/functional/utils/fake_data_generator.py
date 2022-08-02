"""
Генерации фейковых данных, которые используются для тестов.

"""


import json

from elasticsearch import AsyncElasticsearch, RequestError
from elasticsearch.helpers import async_bulk

from ..testdata.fake_models import FakeFilm, FakeGenre, FakePerson


class Generator:

    def __init__(self, es_client):
        self.es_client = es_client
        self.madman_mode = False
        self.test_indices = {'movies': 'movies', 'genres': 'genres', 'persons': 'persons'}
        self.films = []
        self.genres = []
        self.persons = []
        self.films_with_genre = []
        self.films_with_person = []

    async def generate_fake_data(self):
        # Генерация персон, жанров и фильмов
        # (слово test добавляется для разделения тестовых и рабочих данных).
        for index, file_name in self.test_indices.items():
            try:
                await self.create_index(self.es_client, file_name=file_name, index_name=index)
            except RequestError:
                # Тесты на рабочих индексах? Ок...
                self.madman_mode = True

        fake_persons = [FakePerson() for _ in range(20)]
        fake_genres = [
            FakeGenre(name)
            for name in [
                'Фэнтези_test',
                'Комедия_test',
                'Триллер_test',
                'Приключения_test',
                'Боевик_test',
                'Аниме_test',
                'Мюзикл_test',
            ]
        ]
        fake_films = [FakeFilm(fake_persons, fake_genres) for _ in range(10)]

        self.films = self.get_index_data(index='movies', fake_docs=fake_films)
        self.genres = self.get_index_data(index='genres', fake_docs=fake_genres)
        self.persons = self.get_index_data(index='persons', fake_docs=fake_persons)
        # Фильмы с первым жанром.
        genre_name = self.films[0]['_source']['genres'][0]['name']
        self.films_with_genre = self.genre_films(genre_name)
        person_name = self.films[0]['_source']['directors'][0]['name']
        self.films_with_person = self.person_films(person_name)

        await async_bulk(self.es_client, self.films + self.genres + self.persons)

    async def create_index(self, es_client: AsyncElasticsearch, file_name: str, index_name: str) -> None:
        # Создание индексов.
        with open(f'functional/testdata/{file_name}.json', 'r') as index:
            data = json.load(index)
            await es_client.indices.create(index=index_name, body=data)

    def get_index_data(self, index: str, fake_docs: list) -> list:
        # Структура индексов.
        return [
            {
                '_index': index,
                '_id': doc.id,
                '_source': doc.__dict__
            }
            for doc in fake_docs
        ]

    async def remove_fake_data(self):
        if self.madman_mode:
            # Аккуратно удаляем фейковые данные, стараясь не задеть рабочие...
            docs_to_delete = [
                {'_op_type': 'delete', '_index': 'movies', '_id': doc['_id']}
                for doc in self.films
            ]
            docs_to_delete.extend([
                {'_op_type': 'delete', '_index': 'genres', '_id': doc['_id']}
                for doc in self.genres
            ])
            docs_to_delete.extend([
                {'_op_type': 'delete', '_index': 'persons', '_id': doc['_id']}
                for doc in self.persons
            ])
            await async_bulk(self.es_client, docs_to_delete)
        else:
            # Удаление тестовых индексов. Ведь тестовых, да?
            for index in self.test_indices.keys():
                self.es_client.indices.delete(index=index)

    def genre_films(self, genre_name: str) -> list:
        # Список фильмов для теста поиска жанра по id.
        return [
            {'id': film['_id'], 'title': film['_source']['title'], 'imdb_rating': film['_source']['imdb_rating']}
            for film in self.films
            if genre_name in film['_source']['genres_list']
        ]

    def person_films(self, person_name: str) -> dict:
        # Фильмы с человеком в тестовых данных.
        def append_film(film: dict) -> dict:
            return {
                'id': film['_id'],
                'title': film['_source']['title'],
                'imdb_rating': film['_source']['imdb_rating'],
            }

        films_with_person = {'director': [], 'actor': [], 'writer': []}
        for film in self.films:
            persons = {
                'director': film['_source']['directors_names'],
                'actor': film['_source']['actors_names'],
                'writer': film['_source']['writers_names'],
            }
            for k, v in persons.items():
                if person_name in v:
                    films_with_person[k].append(append_film(film))

        return films_with_person
