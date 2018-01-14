from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('',
         views.FileEntityListView.as_view(),
         name='index'),
    path('file/<int:pk>/',
         views.FileEntityDetailView.as_view(),
         name='file-entity-detail'),
    path('new-file',
         views.FileEntityNew,
         name='file-entity-new')
]
