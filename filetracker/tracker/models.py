from django.db import models
from django.urls import reverse


class FileEntity(models.Model):
    """
    Model containing the list of files that are being tracked
    """
    FILE_STATUS = (
        ('n', 'Non-existent'),
        ('t', 'Tracked'),
        ('m', 'Modified')
    )

    name = models.CharField(max_length=200,
                            help_text="Enter a file name")

    status = models.CharField(max_length=1,
                              choices=FILE_STATUS,
                              blank=True,
                              default='n',
                              help_text='Status of the file')

    def get_absolute_url(self):
        return reverse('file-entity-detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class FileHistory(models.Model):

    file_entity = models.ForeignKey('FileEntity',
                                    on_delete=models.CASCADE,
                                    null=False,
                                    related_name='history')

    client_modified = models.DateTimeField(null=True,
                                           blank=True)

    server_modified = models.DateTimeField(null=True,
                                           blank=True)

    inserted = models.DateTimeField(auto_now=True)

    content_hash = models.CharField(max_length=200,
                                    null=True,
                                    blank=True)
