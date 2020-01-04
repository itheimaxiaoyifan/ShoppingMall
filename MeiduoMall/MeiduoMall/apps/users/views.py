from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def tsview(request):
    return HttpResponse('hello django')

def index(request):
    return render(request, 'index.html')