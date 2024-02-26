from django.db import models


# Create your models here.
class Song(models.Model):
    title = models.CharField(unique=True, max_length=200)

    def __str__(self):
        return self.title

    @property
    def midi_path(self):
        return f"data/midi/{self.title}.midi"

    @property
    def xml_path(self):
        return f"data/xml/{self.pk}.xml"

    @property
    def mxl(self):
        with open(self.xml_path, "r") as f:
            mxl = f
        return mxl
