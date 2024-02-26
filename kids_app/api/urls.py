from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

song_list = SongViewSet.as_view({
    'get': 'list',
    'put': 'create',
})

song_detail = SongViewSet.as_view({
    'get': 'retrieve',
})

urlpatterns = [
    path("songs/<int:pk>", song_detail),
    path("songs/", song_list),

]
