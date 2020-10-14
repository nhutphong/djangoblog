from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home_view(request): # *args, **kwargs
    template = 'pages/home.html'
    print(f"{request = }")
    print(f"{request.user = }")
    # return HttpResponse("<h1>Hello World</h1>") # string of HTML code
    return render(request, template, {})