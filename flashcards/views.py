from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello world!")
    #return render(request, "emphasis/index.html")