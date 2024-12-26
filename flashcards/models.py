from django.db import models


class EnglishWords(models.Model):
    word = models.CharField(max_length=20)
    translation = models.CharField(max_length=35)
    level = models.CharField(max_length=2)
    audio_link = models.CharField(max_length=130)
    phonetics = models.CharField(max_length=25, blank=True)
    example = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.word}: {self.translation}"
