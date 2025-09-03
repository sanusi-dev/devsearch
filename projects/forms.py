from django import forms
from .models import *


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags']

        widgets = {
            'tags': forms.CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

    def clean_source_link(self):
        url = self.cleaned_data.get('source_link')

        if url and not url.startswith(('http://', 'https://')):
            url = f'https://{url}'

        return url
    
    def clean_demo_link(self):
        url = self.cleaned_data.get('demo_link')

        if url and not url.startswith(('http://', 'https://')):
            url = f'https://{url}'

        return url

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['body'].widget.attrs.update({'class': 'input', 'placeholder': 'Write your comments here...'})

