from .base_service import Service
from index_models.models import GenreModel

class GenreService(Service):
    def __init__(self):
        Service.__init__(self)
        self.model = GenreModel
