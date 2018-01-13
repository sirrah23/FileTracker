from django.shortcuts import render
from django.views import generic
from .models import FileEntity


class FileEntityListView(generic.ListView):
    # TODO: Access the foreign FileHistory data
    model = FileEntity
    context_object_name = "file_entity_list"
    queryset = FileEntity.objects.all()
    template_name = 'index.html'


class FileEntityDetailView(generic.DetailView):
    model = FileEntity
