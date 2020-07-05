
from django.views.generic import TemplateView, FormView, RedirectView, View

from books.models import *

from random import randint


class Index(RedirectView):
    """
    View to redirect to home page
    """
    url = '/home'


class Home(TemplateView):
    """
    View for List all Books 
    """
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx = super(Home, self).get_context_data(**kwargs)

        books = Book.objects.all()

        ctx['title'] = 'Books Library'
        ctx['heading'] = 'BOOKS'
        ctx['username'] = 'Admin'
        ctx['books'] = books
        ctx['rand'] = randint(100, 999)
        
        return ctx


class BookDetails(TemplateView):
    """
    View for Book Details 
    """
    template_name = 'book-details.html'

    def get_context_data(self, **kwargs):
        ctx = super(BookDetails, self).get_context_data(**kwargs)

        book = Book.objects.get(pk=self.kwargs.get('pk'))
        ctx['title'] = 'Books Library'
        ctx['heading'] = 'Book Details'
        ctx['book'] = book

        ctx['rand'] = randint(100, 999)

        return ctx

