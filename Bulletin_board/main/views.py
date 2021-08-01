from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *


class PublicationsList(ListView):
    model = Publication
    template_name = 'publications.html'
    context_object_name = 'publications'
    ordering = ['-id']
    paginate_by = 15


class PublicationDetail(DetailView):
    model = Publication
    template_name = 'publication.html'
    context_object_name = 'publication'


class PublicationDelete(LoginRequiredMixin, DeleteView):
    template_name = 'publication_delete.html'
    queryset = Publication.objects.all()
    success_url = '/publications'


class PublicationCreate(LoginRequiredMixin, CreateView):
    template_name = 'publication_create.html'
    form_class = PublicationForm

    def get_context_data(self, **kwargs):
        context = super(PublicationCreate, self).get_context_data()
        context['is_create_form'] = True
        return context

    def post(self, request, *args, **kwargs):
        form = PublicationForm(request.POST)
        if form.is_valid():
            publication = Publication.objects.create(
                preview_image=request.FILES['preview_image'],
                title=form.instance.title,
                category=form.instance.category,
                text=form.instance.text,
                author=request.user
            )
            return redirect('publication_detail', pk=publication.pk)


class PublicationUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'publication_create.html'
    form_class = PublicationForm
    success_url = '/publications/'

    def get_object(self, **kwargs):
        return Publication.objects.get(pk=self.kwargs.get('pk'))


class ResponseCreate(LoginRequiredMixin, CreateView):
    template_name = 'response_create.html'
    form_class = ResponseForm

    def post(self, request, *args, **kwargs):
        form = ResponseForm(request.POST)
        if form.is_valid():
            publication = Publication.objects.get(id=request.path.split('/')[-2])
            response = Response.objects.create(
                message=form.instance.message,
                sender=request.user,
                on_publication=publication
            )
            return redirect('publication_detail', pk=publication.pk)


class ResponsesList(ListView):
    model = Response
    template_name = 'responses.html'
    context_object_name = 'responses'
    ordering = ['-id']
    paginate_by = 20

    def get_queryset(self):
        user_publications = Publication.objects.filter(author=self.request.user)
        result = []
        for publication in user_publications:
            responses = self.model.objects.filter(on_publication=publication)
            res_arr = [response for response in responses]
            result.append(*res_arr) if responses else 0
        return result
