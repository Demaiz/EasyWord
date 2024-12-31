from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import *
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


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "flashcards/register.html"
    success_url = reverse_lazy("flashcards:index")

    def form_valid(self, form):
        user = form.save()
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
