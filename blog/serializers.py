from django.contrib.auth.models import User
from .models import Post
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    #url=serializers.HyperlinkedIdentityField(view_name='blog:user-detail')
    email_confirmed=serializers.BooleanField(source='profile.email_confirmed')
    subscribed=serializers.BooleanField(source='profile.subscribed')

    class Meta:
        model =User
        fields=['url', 'username', 'email', 'groups', 'email_confirmed', 'subscribed']

class PostSerializer(serializers.HyperlinkedModelSerializer):
    #url=serializers.HyperlinkedIdentityField(view_name='blog:post-detail')
    class Meta:
        model=Post
        fields=['url', 'pk', 'author', 'title', 'text', 'created_date', 'published_date', 'likes']

