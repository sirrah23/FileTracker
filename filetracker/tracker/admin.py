from django.contrib import admin
from .models import FileEntity, FileHistory


class FileHistoryInline(admin.TabularInline):
    list_display = ('content_hash', 'client_modified', 'server_modified')
    model = FileHistory
    ordering = ['-inserted']


@admin.register(FileEntity)
class FileEntityAdmin(admin.ModelAdmin):
    inlines = [FileHistoryInline]
