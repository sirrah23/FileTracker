from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import NewFileEntityForm
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
    context_object_name = "file_entity"
    template_name = "file-entity-detail.html"


def FileEntityNew(request):
    if request.method == 'POST':
        print("Post has been seen!")
        form = NewFileEntityForm(request.POST)
        if form.is_valid():
            fe = FileEntity(name=form.cleaned_data['name'])
            fe.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = NewFileEntityForm()
        return render(request,
                      'file-entity-new.html',
                      {'form': form})

