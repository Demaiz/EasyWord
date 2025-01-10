from django.db import models
from django.contrib.auth.models import User


class EnglishWords(models.Model):
    word = models.CharField(max_length=20)
    translation = models.CharField(max_length=35)
    level = models.CharField(max_length=2)
    audio_link = models.CharField(max_length=130)
    phonetics = models.CharField(max_length=25, blank=True)
    example = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.word}: {self.translation}"


class UserWordSelection(models.Model):
    STATUS_CHOICES = [
        ("selected", "Selected"),    # user can start to learn this word
        ("learning", "Learning"),    # user currently learning this word
        ("known", "Already known"),  # user already know this word
        ("repeating", "Repeating"),  # user learned this word and now repeating it
        ("learned", "Fully learned") # user learned this word and repeated it
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    english_words = models.ForeignKey(EnglishWords, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="selected")


class RepeatWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    english_words = models.ForeignKey(EnglishWords, on_delete=models.CASCADE)
    date = models.DateTimeField()
    # a word needs to be repeated multiple times to be considered fully learned
    times_repeated = models.PositiveSmallIntegerField(default=0)
