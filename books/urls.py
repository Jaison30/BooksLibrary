from django.conf.urls import url, include
from books.views import *

urlpatterns = [
	url(r'^$', Index.as_view(), name='index'),
    url('home/', Home.as_view(), name='home'),
    url(r'^book/(?P<pk>\d+)$', BookDetails.as_view(), name='book-details'),
]