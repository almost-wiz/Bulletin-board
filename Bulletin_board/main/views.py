from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *


class PublicationsList(ListView):
    model = Publication
    template_name = 'publications.html'
    context_object_name = 'publications'
    ordering = ['-id']
    paginate_by = 12


class PublicationDetail(DetailView):
    model = Publication
    template_name = 'publication.html'
    context_object_name = 'publication'


class PublicationDelete(LoginRequiredMixin, DeleteView):
    template_name = 'publication_delete.html'
    queryset = Publication.objects.all()
    success_url = '/publications'

