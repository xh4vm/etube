"""
Генерации фейковых данных, которые используются для тестов.

"""


import json
from elasticsearch.helpers import async_bulk

from ..testdata.fake_models import FakeFilm, FakeGenre, FakePerson


class Generator:

    def __init__(self, es_client):
        self.es_client = es_client
        # self.madman_mode = False
        # self.test_indices = {'movies': 'movies', 'genres': 'genres', 'persons': 'persons'}
        self.films = []
        self.genres = []
        self.persons = []

    async def generate_fake_data(self):
        fake_genres, fake_persons, fake_films = [], [], []

        #TODO refactoring
        with open(f'/opt/tests/functional/testdata/json/genres.json', 'r') as fd:
            genres_fake_data = json.load(fd)

        with open(f'/opt/tests/functional/testdata/json/persons.json', 'r') as fd:
            persons_fake_data = json.load(fd)

        with open(f'/opt/tests/functional/testdata/json/movies.json', 'r') as fd:
            movies_fake_data = json.load(fd)

        for genre in genres_fake_data:
            fake_genres.append(FakeGenre(**genre))
            
        for person in persons_fake_data:
            fake_persons.append(FakePerson(**person))

        for movies in movies_fake_data:
            fake_films.append(FakeFilm(**movies))
        # Генерация персон, жанров и фильмов
        # (слово test добавляется для разделения тестовых и рабочих данных).

        # fake_persons = [FakePerson() for _ in range(20)]
        # fake_genres = [
        #     FakeGenre(name)
        #     for name in [
        #         'Фэнтези_test',
        #         'Комедия_test',
        #         'Триллер_test',
        #         'Приключения_test',
        #         'Боевик_test',
        #         'Аниме_test',
        #         'Мюзикл_test',
        #     ]
        # ]
        # fake_persons = [FakePerson() for _ in range(20)]
        # fake_genres=[]
        # fake_films = []
        # # fake_films = [FakeFilm(fake_persons, fake_genres) for _ in range(10)]

        #TODO refactoring
        self.films = self.get_index_data(index='movies', fake_docs=fake_films)
        self.genres = self.get_index_data(index='genres', fake_docs=fake_genres)
        self.persons = self.get_index_data(index='persons', fake_docs=fake_persons)

        await async_bulk(self.es_client, self.films + self.genres + self.persons)

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

    #TODO delete by term key '::test::'
    async def remove_fake_data(self):
        # if self.madman_mode:
        # Аккуратно удаляем фейковые данные, стараясь не задеть рабочие...
        docs_to_delete = [
            {'_op_type': 'delete', '_index': 'movies', '_id': doc['_id']} for doc in self.films
        ]
        docs_to_delete.extend([{'_op_type': 'delete', '_index': 'genres', '_id': doc['_id']} for doc in self.genres])
        docs_to_delete.extend([{'_op_type': 'delete', '_index': 'persons', '_id': doc['_id']} for doc in self.persons])
        await async_bulk(self.es_client, docs_to_delete)
        # else:
        #     # Удаление тестовых индексов. Ведь тестовых, да?
        #     for index in self.test_indices.keys():
        #         self.es_client.indices.delete(index=index)
