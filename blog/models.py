from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from re import sub
from django.core.validators import RegexValidator

def serialize_url(url):
    return str.lower(sub(r'[^a-zA-Zа-яА-Я0-9 ]', r'', url.replace("-", " ")).replace(" ", "-"))


def split_str(string):
    return set(str.upper(sub(r'[^a-zA-Zа-яА-Я0-9 ]', r'', string).replace("  ", " ")).split(" "))

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscribed=models.BooleanField(default=False)
    email_confirmed=models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/', default="default_profile.png")
    date_of_birth=models.DateField(blank=True, default="2000-01-01", null=True)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 12 digits allowed.")
    mobile = models.CharField(validators=[phone_regex], max_length=12, blank=True) # validators should be a list

    description=models.CharField(max_length=100, default="You can contact me through my mail.", blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)
        instance.profile.save()


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='post_likes')

    def get_total_likes(self):
        return self.likes.count()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title

@receiver(post_save, sender=Post)
def create_post(sender, instance, created, **kwargs):
        if created:
            for subscriber in BlogSubscriber.objects.all():
                Notification.objects.create(subscriber=subscriber.blog_subscriber, post=instance)

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment=True
        self.save()

    def __str__(self):
        return self.text

@receiver(post_save, sender=Comment)
def create_comment(sender, instance, created, **kwargs):
        if created:
            for subscriber in BlogSubscriber.objects.all():
                Notification.objects.create(subscriber=subscriber.blog_subscriber, comment=instance)

class BlogSubscriber(models.Model):
    blog_subscriber=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Notification(models.Model):
    subscriber=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    post=models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    comment=models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    status=models.BooleanField(default=False)

class Index(models.Model):
    word=models.CharField(max_length=100)
    post=models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    def create(self):
        posts=Post.objects.all()
        for post in posts:
            self.add(post)
            print("Indexes for {0} ({1}) created".format(post, post.pk))
        print("All indexes created")
    
    @classmethod
    def add(ind, post):
        words=split_str(post.text + " "+ post.title)
        for word in words:
            if len(word)>2:
                if len(ind.objects.filter(word=word, post=post))<1:
                    ind.objects.create(word=word, post=post)

    def delete(self):
        self.objects.all().delete()
        print("All indexes deleted")

    @staticmethod
    def find(search_request):
        search_words=split_str(search_request)
        posts_pk_list=[]

        
        for word in search_words:
            pk_list=set([index.post.pk for index in Index.objects.filter(word=word)])
            if pk_list:
                posts_pk_list.append(pk_list)
            else:
                pass
        
        if posts_pk_list:
            intersection_pk=posts_pk_list[0]
            for post_pk in range(len(posts_pk_list)-1):
                intersection_pk=posts_pk_list[post_pk] & posts_pk_list[post_pk+1]
            return [Post.objects.get(pk=pk) for pk in intersection_pk]
        else:
            return []



