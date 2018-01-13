from django.contrib import admin
from .models import FileEntity, FileHistory


admin.site.register(FileEntity)
admin.site.register(FileHistory)
