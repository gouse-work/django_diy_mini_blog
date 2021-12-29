from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class CommentCreateForm(forms.Form):
    description=forms.CharField(help_text='Enter comment about blog here.',max_length=1000,widget=forms.Textarea())

    def clean_description(self):
        data=self.cleaned_data['description']

        if len(data) > 1000:
            raise ValidationError(_("Invalid description-length greater than 1000"))

        return  data



