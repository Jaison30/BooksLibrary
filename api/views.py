# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from rest_framework import authentication, permissions, viewsets
from rest_framework.pagination import  PageNumberPagination
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
    SAFE_METHODS
)
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.generics import RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import *

# Create your views here.


class DefaultsMixin(object):
    """docstring for DefaultsM"""
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
        )
    permission_classes = (
        permissions.IsAuthenticated,
        )

""" Authentication Views """


class UserLoginAPIView(GenericAPIView):

    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None or len(username) == 0 or len(password) == 0:
            return Response({'status': 'failed','error': 'Please provide both username and password'},
                            status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password) 
        if not user:
            return Response({'status': 'failed','error': 'Invalid Credentials'},
                            status=HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                data=TokenSerializer(token).data,
                status=HTTP_200_OK,
            )
        else:
            return Response(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class UserCreate(APIView):

    serializer_class = UserSerializer

    def get(self, request, format=None):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):

        user_data = request.data

        if User.objects.filter(username=user_data.get('username')).exists():
            return Response({'status': 'failed', 'error': 'username already exists'})
        elif User.objects.filter(email=user_data.get('email')).exists():
            return Response({'status': 'failed', 'error': 'email already exists'})
        else:
            user_obj = User.objects.create_user(
                username = user_data.get('username'),
                email = user_data.get('email'),
                password=user_data.get('password')
            )
         
        return Response({'status': 'success', 'msg': 'User Created Successfully'})


""" Authentication Views End """


class BookCreate(DefaultsMixin,  ListCreateAPIView):
    """ API to create Book
    """
    permission_classes = (IsAuthenticated, )
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    

class PagesPagination(PageNumberPagination):
    """ To set default book list pagination size
    """
    page_size = 10


class BookListAPIView(DefaultsMixin, ListCreateAPIView):
    """ API to show all books list
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    pagination_class = PagesPagination


class BorrowedBookListAPIView(DefaultsMixin, APIView):
    """ API to Borrow book API
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BorrowBookSerializer
    pagination_class = PagesPagination

    def get(self, request, format=None):
        queryset = BorrowedBook.objects.all()
        serializer = BorrowBookSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

    	dataset = request.data
        serializer = BorrowBookSerializer(data=dataset)
        if serializer.is_valid():

            book_id = dataset.get('book')
            date = dataset.get('date')

            borrowed_book = BorrowedBook()
            borrowed_book.user = self.request.user
            borrowed_book.book = Book.objects.get(id=book_id)
            borrowed_book.date = date
            borrowed_book.save()

            book = Book.objects.get(id=book_id)
            book.book_count = int(book.book_count) + 1
            book.save()

            return Response({"Status": "1", "Message": "Borrow Book Successfully created"})
        return Response({"Status": "1", "Message": serializer.errors})
    

class BorrowedBooks(DefaultsMixin, ListAPIView):
    """ API to get borrowed books list by user
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BorrowBookSerializer
    queryset = BorrowedBook.objects.all()
    pagination_class = PagesPagination

    def get_queryset(self):

        user = self.request.user.username
        userobj = User.objects.get(username=user)

        data_queryset = BorrowedBook.objects.filter(user=userobj)

        return data_queryset

