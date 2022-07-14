from config.routers import OptionalSlashRouter
from django.urls import include, path

from .views import MoviesApi

router = OptionalSlashRouter()
router.register('movies', MoviesApi, basename='movies')

urlpatterns = [
    path('', include(router.urls)),
]
