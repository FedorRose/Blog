from django import forms
from .models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'last_name', 'text')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'}),
            'text': forms.Textarea(attrs={'cols': 45, 'rows': 7, 'placeholder': 'Message'})
        }
