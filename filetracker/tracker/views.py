from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from .forms import NewFileEntityForm, FileEntityHandleForm
from django.views import generic, View
from django.views.generic.detail import SingleObjectMixin
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
    template_name = 'index.html'

    def get_queryset(self):
        qs = self.model._default_manager.get_queryset()
        order = ['m', 't', 'p', 'n']
        return sorted(qs, key=lambda q: order.index(q.status))


class FileEntityDetailView(generic.DetailView):
    model = FileEntity
    context_object_name = "file_entity"
    template_name = "file-entity-detail.html"

    def get_context_data(self, **kwargs):
        context = super(FileEntityDetailView, self).get_context_data(**kwargs)
        context['form'] = FileEntityHandleForm()
        return context


class FileEntityHandle(SingleObjectMixin, generic.FormView):
    template_name = 'file-entity-detail.html'
    form_class = FileEntityHandleForm
    model = FileEntity

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Update the status of the file to tracked...no need for any validation
        self.object.status = 't'
        self.object.save()
        return super(FileEntityHandle, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('file-entity-detail', kwargs={'pk': self.object.pk})


class FileEntityDetail(View):
    """
    When you do a GET request it makes the FileEntityDetailView available
    to you which presents the information associated with the current FileEntity.

    When you perform a POST request it allows you to update the status of the
    particular FileEntity from Modified to Handled.
    """

    def get(self, request, *args, **kwargs):
        view = FileEntityDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = FileEntityHandle.as_view()
        return view(request, *args, **kwargs)


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
