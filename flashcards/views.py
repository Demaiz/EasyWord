from calendar import month

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import JsonResponse
from datetime import timedelta
from .forms import *
from .models import *
import json
from django.utils import timezone
from django.db.models import F


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


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "flashcards/register.html"
    success_url = reverse_lazy("flashcards:index")

    def form_valid(self, form):
        user = form.save() # add new user to database

        # mark all words as selected for this user
        english_words = EnglishWords.objects.all()
        data = []
        for word in english_words:
            data.append(UserWordSelection(user=user, english_words=word))
        UserWordSelection.objects.bulk_create(data)

        login(self.request, user) # auto login
        return redirect("flashcards:index")


class LoginUser(LoginView):
    form_class = AuthenticationUserForm
    template_name = "flashcards/login.html"

    def get_success_url(self):
        return reverse_lazy("flashcards:index")


def logout_user(request):
    logout(request)
    return redirect("flashcards:login")

@login_required # if user is not authenticated - page 404
def learn(request):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    if is_ajax:
        # GET request is used for sending data to js file
        if request.method == "GET":
            # get words with status "learning" from db
            learning_words = list(EnglishWords.objects.filter(userwordselection__user=request.user, userwordselection__status="learning").order_by("?").values())
            # get words with status "selected" from db
            number_of_selected_words = 10 - len(learning_words) # total number of words is 10
            # variable sometimes can be negative because of race condition between AJAX requests
            if number_of_selected_words < 0:
                number_of_selected_words = 0
            selected_words = list(EnglishWords.objects.filter(userwordselection__user=request.user, userwordselection__status="selected").order_by("?").values()[:number_of_selected_words])

            context = {
                "selected_words": selected_words,
                "learning_words": learning_words
            }
            return JsonResponse(context)  # send words to js file
        # POST request is used for getting data from js file
        if request.method == "POST":
            data = json.loads(request.POST.get("main"))
            # update word status
            UserWordSelection.objects.filter(user=request.user, english_words=data["word_id"]).update(status=data["status"])

            if data["status"] == "repeating":
                word = EnglishWords.objects.get(id=data["word_id"])
                RepeatWord.objects.create(user=request.user, english_words=word, date=timezone.now())
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "invalid request"}, status=400)
    else:
        # if request is not AJAX, render page
        return render(request, "flashcards/learn.html")

@login_required # if user is not authenticated - page 404
def repeat(request):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    if is_ajax:
        # a word will be displayed to the user at increasing intervals
        # each time the user repeats the word, the interval increases
        # word counts as fully learned if user repeated it 6 times
        intervals = [
            timedelta(minutes=20),
            timedelta(hours=2),
            timedelta(days=1),
            timedelta(days=3),
            timedelta(weeks=1),
            timedelta(weeks=2),
            timedelta(weeks=4)
        ]
        # GET request is used for sending data to js file
        if request.method == "GET":
            word_ids = []
            all_repeat_words = RepeatWord.objects.filter(user=request.user)
            # find words to repeat
            for word in all_repeat_words:
                if word.date + intervals[word.times_repeated] < timezone.now():
                    word_ids.append(word.english_words_id)

            repeat_words = list(EnglishWords.objects.filter(id__in=word_ids).values())
            return JsonResponse({"repeat_words": repeat_words})
        # POST request is used for getting data from js file
        elif request.method == "POST":
            data = json.loads(request.POST.get("main"))
            repeat_word = RepeatWord.objects.filter(user=request.user, english_words = data["word_id"])
            # if user repeated word 6 times, mark it as "fully learned" and remove it from RepeatWord
            if repeat_word[0].times_repeated == 6:
                UserWordSelection.objects.filter(user=request.user, english_words = data["word_id"]).update(status="learned")
                repeat_word.delete()
            # increment times_repeated field and update timer
            else:
                repeat_word.update(times_repeated=F("times_repeated") + 1, date=timezone.now())
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "invalid request"}, status=400)
    else:
        # if request is not AJAX, render the page
        return render(request, "flashcards/repeat.html")
