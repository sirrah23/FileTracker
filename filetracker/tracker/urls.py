from django.urls import path

from . import views

urlpatterns = [
    path('',
         views.FileEntityListView.as_view(),
         name='index'),
    path('file/<int:pk>/',
         views.FileEntityDetail.as_view(),
         name='file-entity-detail'),
    path('new-file',
         views.FileEntityNew,
         name='file-entity-new'),
    path('delete-file/<int:pk>',
         views.FileEntityDelete.as_view(),
         name='file-entity-delete')
]
