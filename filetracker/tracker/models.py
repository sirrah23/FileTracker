from django.db import models
from django.urls import reverse


class FileEntity(models.Model):
    """
    Model containing the list of files that are being tracked
    """
    name = models.CharField(max_length=200,
                            help_text="Enter a file name")

    def get_absolute_url(self):
        return reverse('file-entity-detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class FileHistory(models.Model):

    FILE_STATUS = (
        ('n', 'Non-existent'),
        ('t', 'Tracked'),
        ('m', 'Modified')
    )

    file_entity = models.ForeignKey('FileEntity',
                                    on_delete=models.CASCADE,
                                    null=False,
                                    related_name='history')

    client_modified = models.DateField(null=True,
                                       blank=True)

    server_modified = models.DateField(null=True,
                                       blank=True)

    content_hash = models.CharField(max_length=200,
                                    null=True,
                                    blank=True)

    status = models.CharField(max_length=1,
                              choices=FILE_STATUS,
                              blank=True,
                              default='m',
                              help_text='Status of the file')
