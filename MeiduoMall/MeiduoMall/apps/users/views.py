from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import CreateUserSerializer, UserDetailSerializer


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


class UserDetailView(RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
