from django import forms
from django.forms import ModelForm
from .models import Publication, Response


class PublicationForm(ModelForm):

    class Meta:
        model = Publication
        fields = ['preview_image', 'title', 'category', 'text']

    def __init__(self, *args, **kwargs):
        super(PublicationForm, self).__init__(*args, **kwargs)
        self.fields['preview_image'].required = False


class ResponseForm(ModelForm):

    message = forms.CharField(
        widget=forms.Textarea(),
    )

    class Meta:
        model = Response
        fields = ['message']
