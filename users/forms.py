from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *



class UserRegistrationForm(UserCreationForm):
    name = forms.CharField()
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'name')

    
    def clean_email(self):
        email = self.cleaned_data['email']
        return email.lower()
    
    def clean_name(self):
        name = self.cleaned_data['name']
        return name.lower()
    
    def clean_username(self):
        username = self.cleaned_data['username']
        return username.lower()

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})