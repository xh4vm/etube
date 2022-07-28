films = [
    {
        '_index': 'movies',
        '_id': 123,
        '_source': {
            'id': 123,
            'title': 'Test Movie',
            'imdb_rating': 9.8,
            'description': 'Test Movie description.',
            'directors_names': ['director 1'],
            'actors_names': ['actor 1', 'actor 2', 'actor 2'],
            'writers_names': ['writer 1', 'writer 2'],
            'genres_list': ['genre 1', 'genre 2'],
            'directors': [{'id': 456, 'name': 'director 1'}],
            'genres': [{'id': 7, 'name': 'genre 1'}, {'id': 8, 'name': 'genre 2'}],
        }
    }
]