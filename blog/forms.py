from django import forms
from .models import Post, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Provide a valid email address')

    class Meta:
        model=User
        fields=('username', 'email', 'password1', 'password2')

class PostForm(forms.ModelForm):

    class Meta:
        model =Post
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):

    class Meta:
        model=Comment
        fields = ('author', 'text')