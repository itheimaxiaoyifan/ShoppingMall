from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import CreateUserSerializer


def tsview(request):
    return HttpResponse('hello django')


def index(request):
    return render(request, 'test.html')


class TestView2(APIView):
    def get(self, request):
        return Response({'mes': 'get请求'})

    def post(self, request):
        return Response({'mes': 'post请求'})


# usernames/(?P<username>\w{5,20})/count/
class UsernameCountView(APIView):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        data = {
            'username': username,
            'count': count
        }
        return Response(data)


class CreateUserView(CreateAPIView):
    serializer_class = CreateUserSerializer
