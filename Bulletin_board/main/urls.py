from django.urls import path
from .views import *


urlpatterns = [
    path('publications/', PublicationsList.as_view()),
    path('publications/<int:pk>', PublicationDetail.as_view()),
    path('publications/<int:pk>/delete', PublicationDelete.as_view()),
]