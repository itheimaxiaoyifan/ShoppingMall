from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView


def tsview(request):
    return HttpResponse('hello django')


def index(request):
    return render(request, 'index.html')


class TestView2(APIView):
    def get(self, request):
        a = 1/0

        return Response({'mes': 'get请求','a':a})

    def post(self, request):
        return Response({'mes': 'post请求'})
