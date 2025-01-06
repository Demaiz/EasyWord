from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import JsonResponse
from .forms import *
from .models import *
import json


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
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "invalid request"}, status=400)
    else:
        # if request is not AJAX render page
        return render(request, "flashcards/learn.html")
