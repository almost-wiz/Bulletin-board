from .models import Response, Publication
import django_filters


class ResponsesFilter(django_filters.FilterSet):
    on_publication = django_filters.ChoiceFilter(choices=None)

    class Meta:
        model = Response
        fields = ['on_publication', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = kwargs['request']
        if request.user.is_authenticated:
            user = request.user
            choices = Publication.objects.filter(author=user)
            result = [(choice.id, choice) for choice in choices]
            self.filters['on_publication'].extra.update({'choices': result})
