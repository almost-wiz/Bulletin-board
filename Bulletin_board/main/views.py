from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.mail import send_mail
from django.contrib.auth.models import User
from Bulletin_board.email_data import default_from_email
from .forms import *
from .filters import *


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

    def get_object(self, **kwargs):
        publication = Publication.objects.get(pk=self.kwargs.get('pk'))
        if self.request.user != publication.author:
            raise PermissionDenied
        return publication


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
        publication = Publication.objects.get(pk=self.kwargs.get('pk'))
        if self.request.user != publication.author:
            raise PermissionDenied
        return publication


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


class ResponsesFilter(LoginRequiredMixin, ListView):
    filterset_class = ResponsesFilter
    model = Response
    template_name = 'responses.html'
    context_object_name = 'responses'
    ordering = ['-id']
    paginate_by = 20

    def get_queryset(self):
        queryset = Response.objects.filter(on_publication__author=self.request.user, accepted=False)
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset, request=self.request)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super(ResponsesFilter, self).get_context_data(**kwargs)
        context['responses_length'] = self.filterset.qs.count()
        context['filter'] = self.filterset_class(self.request.GET, queryset=self.get_queryset(), request=self.request)
        return context


@login_required
def accept_response(request, **kwargs):
    response = Response.objects.get(id=request.path.split('/')[-2])
    response.accepted = True
    response.save()

    return redirect('/responses')


@login_required
def delete_response(request, **kwargs):
    response = Response.objects.get(id=request.path.split('/')[-2])
    response.delete()

    return redirect('/responses')


def contact_view(request):
    if not request.user.is_staff:
        raise PermissionDenied

    if request.method == 'GET':
        form = MailingForm()
    elif request.method == 'POST':
        form = MailingForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            for user in User.objects.all():
                send_mail(subject, message, default_from_email, [user.email])
            return redirect('publications/')
    else:
        raise ObjectDoesNotExist
    return render(request, "mailing.html", {'form': form})
