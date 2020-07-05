from django.conf.urls import url, include
from .views import *

urlpatterns = [

    url('login/', UserLoginAPIView.as_view(), name='user-login'),
    url('user-create/', UserCreate.as_view(), name='user-create'),
    url('book-create/', BookCreate.as_view(), name='book-create'),
    url('borrow-books/', BorrowedBookListAPIView.as_view(), name='borrow-books'),
    url('book-list/', BookListAPIView.as_view(), name='book-list'),
    url('borrowed-books-list/', BorrowedBooks.as_view(), name='borrowed-books-list'),
    
]