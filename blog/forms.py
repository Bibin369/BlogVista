from django import forms
from django.forms import fields, widgets
from .models import Post, Comment

# forms.py

from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'problem']


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control custom-txt','cols':'40','rows':'3'}), label='')
    class Meta:
        model = Comment
        fields = ['body',]