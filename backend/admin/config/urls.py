from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('movies.api.urls')),
]
