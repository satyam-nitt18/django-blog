from django import forms
from .models import Post, Comment, Profile
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
        fields = ('text',)


class ProfileForm(forms.ModelForm):
    YEARS=[x for x in range(1940, 2010)]
    date_of_birth=forms.DateField(label='Set Date of birth: ', initial="2000-01-01", widget=forms.SelectDateWidget(years=YEARS))
    mobile=forms.RegexField(label='Mobile number: ', regex=r'^\+?1?\d{9,15}$', error_messages = {'Required': "Phone number must be entered in the format: '+999999999'. Up to 12 digits allowed."}, required=False)
    image=forms.ImageField(label='Select Image: ')
    description=forms.CharField(label='Description: ', required=False, max_length=200)

    class Meta:
        model=Profile
        fields=('date_of_birth', 'mobile', 'description', 'image')

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Email: ', max_length=254, help_text='Required. Provide a valid email address')
    username=forms.CharField(label='Username: ', max_length=150)
    class Meta:
        model=User
        fields=('username', 'email',)