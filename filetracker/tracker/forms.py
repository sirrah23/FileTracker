from django import forms
from django.core.exceptions import ValidationError
from .models import FileEntity


class NewFileEntityForm(forms.Form):
    name = forms.CharField(
        help_text="Enter the name for the new file that you want to track"
    )

    def check_name(self):
        data = self.cleaned_data['name']

        if len(data) == 0:
            raise ValidationError('No valid filename provided')

        # TODO: Is this the right place to be doing this validation?
        if FileEntity.objects.filter(name=data).count() != 0:
            raise ValidationError('File already exists in system')

        return data


class FileEntityHandleForm(forms.Form):
    """
    This form is just a button on the UI for changing a file
    status from Modified to Tracked.
    """
    pass
