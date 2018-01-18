from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from .forms import NewFileEntityForm
from django.views import generic
from django.views.generic.edit import DeleteView
from .models import FileEntity

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from dbxcelery.tasks import update_file_metadata


class FileEntityListView(generic.ListView):
    # TODO: Access the foreign FileHistory data
    model = FileEntity
    context_object_name = "file_entity_list"
    queryset = FileEntity.objects.all()
    template_name = 'index.html'


class FileEntityDetailView(generic.DetailView):
    model = FileEntity
    context_object_name = "file_entity"
    template_name = "file-entity-detail.html"


def FileEntityNew(request):
    if request.method == 'POST':
        form = NewFileEntityForm(request.POST)
        if form.is_valid():
            fe = FileEntity(name=form.cleaned_data['name'])
            fe.save()
            update_file_metadata.delay(form.cleaned_data['name'])
            return HttpResponseRedirect(reverse('index'))
    else:
        form = NewFileEntityForm()
        return render(request,
                      'file-entity-new.html',
                      {'form': form})


class FileEntityDelete(DeleteView):
    model = FileEntity
    context_object_name = "file_entity"
    template_name = "file-entity-delete.html"
    success_url = reverse_lazy('index')
