from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from .models import *


def index(request):
    return render(request, "flashcards/index.html")

def dictionary(request):
    paginator = Paginator(EnglishWords.objects.all(), 60)
    page = request.GET.get("page")
    english_words = paginator.get_page(page)

    # get indexes of next 2 and previous 2 pages for pagination
    current_page = english_words.number
    start_page_range = max(current_page - 2, 2)
    end_page_range = min(current_page + 3, paginator.num_pages)
    page_range = range(start_page_range, end_page_range)

    context = {"english_words": english_words, "page_range": page_range}
    return render(request, "flashcards/dictionary.html", context)
