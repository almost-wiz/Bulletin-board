from django.urls import path
from .views import *


urlpatterns = [
    path('', PublicationsList.as_view()),
    path('publications/', PublicationsList.as_view()),
    path('publications/create', PublicationCreate.as_view()),
    path('publications/<int:pk>', PublicationDetail.as_view(), name='publication_detail'),
    path('publications/<int:pk>/edit', PublicationUpdate.as_view(), name='publication_update'),
    path('publications/<int:pk>/delete', PublicationDelete.as_view()),
    path('publications/<int:pk>/respond', ResponseCreate.as_view()),
    path('responses', ResponsesList.as_view())
]
