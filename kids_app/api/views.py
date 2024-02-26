import string
import random

from django.conf import settings
from django.shortcuts import get_object_or_404

from infrastructure import basic_pitcher, music21_renderer
from songs.models import Song
from songs.serializers import SongSerializer, SongMXLSerializer
from rest_framework import viewsets
from rest_framework.response import Response

from songs.utlilts import handle_uploaded_file

SRC_EXT = {
    "midi": "midi",
    "image": "png",
}


class SongViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Song.objects.all()
        serializer = SongSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Song.objects.all()
        song = get_object_or_404(queryset, pk=pk)
        serializer = SongMXLSerializer(song)
        return Response(serializer.data)

    def create(self, request):
        session_id = request.session.session_key
        if session_id is None:
            session_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        body = request["POST"]

        if "src" in request["GET"].keys():
            src = request["GET"].keys()
        else:
            src = "midi"

        song = Song(title=body["title"])

        file = request.FILES["file"]
        file_url = handle_uploaded_file(file, f"{src}/{session_id}/",
                                        filename=f"{song.pk}.{SRC_EXT[src]}")
        if src == "image":
            pass
            # TODO: do magic with img2sheet

        elif src == "midi":
            try:
                midi_data = basic_pitcher.from_file(file_url.replace("/", "", 1))
                midi_data = basic_pitcher.save_to_data(midi_data, file=song.pk)
            except FileNotFoundError:
                return Response({"error": "File not found"}, status=404)

        xml_path = music21_renderer(music21_renderer, song.xml_path)
        song.save()

        serializer = SongMXLSerializer(song)
        return Response(serializer.data, status=201)
