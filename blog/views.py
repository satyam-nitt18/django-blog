from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment, Profile, Index, BlogSubscriber, Notification
from .forms import PostForm, CommentForm, SignUpForm, UserUpdateForm, ProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.views import generic
from .tokens import account_activation_token
from django.http import HttpResponseRedirect
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, PostSerializer

# Create your views here.
def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    
    if request.user.is_authenticated:
        new_not=Notification.objects.filter(subscriber=request.user, status=False).count()
        return render(request, 'blog/post_list.html', {'posts': posts, 'notifications': Notification.objects.filter(subscriber=request.user).order_by('-pk'), 'new_not': new_not})
    else:
        return render(request, 'blog/post_list.html', {'posts': posts, 'notifications': [], 'new_not': 0})


def post_detail(request, pk):
    post=get_object_or_404(Post, pk=pk)
    
    if request.user.is_authenticated:  
        for n in Notification.objects.filter(post=post, subscriber=request.user):
            n.status=True
            n.save()
        for comment in post.comments.all():
            for n in Notification.objects.filter(comment=comment, subscriber=request.user):
                n.status=True
                n.save()     

        new_not=Notification.objects.filter(subscriber=request.user, status=False).count()
        return render(request, 'blog/post_detail.html', {'post': post, 'is_user_liked': post.likes.filter(id=request.user.id).exists(), 'notifications': Notification.objects.filter(subscriber=request.user).order_by('-pk'), 'new_not': new_not})
    else:
        return render(request, 'blog/post_detail.html', {'post': post, 'is_user_liked': 0, 'notifications': [], 'new_not': 0})
    
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    new_not=Notification.objects.filter(subscriber=request.user, status=False).count()
    return render(request, 'blog/post_edit.html', {'form': form, 'notifications': Notification.objects.filter(subscriber=request.user).order_by('-pk'), 'new_not': new_not})

@login_required
def post_edit(request, pk):
    post=get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.created_date=timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form=PostForm(instance=post)
    new_not=Notification.objects.filter(subscriber=request.user, status=False).count()
    return render(request, 'blog/post_edit.html', {'form':form, 'notifications': Notification.objects.filter(subscriber=request.user).order_by('-pk'), 'new_not': new_not})

@login_required
def post_draft_list(request):
    posts=Post.objects.filter(published_date__isnull=True).order_by('created_date')
    new_not=Notification.objects.filter(subscriber=request.user, status=False).count()
    return render(request, 'blog/post_draft_list.html', {'posts': posts, 'notifications': Notification.objects.filter(subscriber=request.user).order_by('-pk'), 'new_not': new_not})

@login_required
def post_publish(request, pk):
    post=get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post=get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog:post_list')

@login_required
def add_comment_to_post(request, pk):
    post=get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid() :
            comment = form.save(commit=False)
            comment.post=post
            comment.author=request.user.username
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    new_not=Notification.objects.filter(subscriber=request.user, status=False).count()
    return render(request, 'blog/add_comment_to_post.html', {'form': form, 'notifications': Notification.objects.filter(subscriber=request.user).order_by('-pk'), 'new_not': new_not})

@login_required           
def comment_approve(request, pk):
    comment=get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment=get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('blog:post_detail', pk=comment.post.pk)

def signup(request):

    if request.method == 'POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_superuser=False
            user.is_active=False
            user.save()
            current_site=get_current_site(request)
            subject='Activate your Django Blog Account'
            message=render_to_string('blog/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('blog:account_activation_sent')
    else:
        form=SignUpForm()
    if request.user.is_authenticated:       
        new_not=Notification.objects.filter(subscriber=request.user, status=False).count()
        return render(request, 'registration/signup.html', {'form': form, 'notifications': Notification.objects.filter(subscriber=request.user).order_by('-pk'), 'new_not': new_not})
    else:
        return render(request, 'registration/signup.html', {'form': form, 'notifications': [], 'new_not': 0})




def account_activation_sent(request):
    return render(request, 'blog/account_activation_sent.html', {})

def activate(request, uidb64, token):
    try:
        uid=force_text(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user=None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active=True
        user.profile.email_confirmed=True
        user.save()
        login(request, user)
        return redirect('blog:post_list')
    else:
        return render(request, 'blog/account_activation_invalid.html')

@login_required
def PostLike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('blog:post_detail', pk=post.pk)

@login_required
def SubscribeOnBlogNotificationsView(request):
    request.user.profile.subscribed=True
    request.user.save()
    BlogSubscriber.objects.create(blog_subscriber=request.user)
    return HttpResponseRedirect('/')

@login_required
def UnsubscribeOnBlogNotificationsView(request):
    request.user.profile.subscribed=False
    request.user.save()
    Notification.objects.filter(subscriber=request.user).delete()
    BlogSubscriber.objects.filter(blog_subscriber__pk=request.user.pk).delete()
    return HttpResponseRedirect('/')

@login_required
def NotificationDeleteView(request, pk):
    Notification.objects.get(pk=pk).delete()
    # redirecting to the previous page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def user_detail(request, username):
    u=User.objects.get(username=username)
    posts=Post.objects.filter(author=u, published_date__lte=timezone.now()).order_by('-published_date')
    if request.user.is_authenticated:
        new_not=Notification.objects.filter(subscriber=request.user, status=False).count()
        return render(request, 'blog/user_detail.html', {'user': u, 'posts': posts, 'notifications': Notification.objects.filter(subscriber=request.user).order_by('-pk'), 'new_not': new_not})
    else:
        return render(request, 'blog/post_draft_list.html', {'user': u, 'posts': posts, 'notifications': [], 'new_not': 0})

@login_required
def password_change(request):
    if request.method == 'POST':
        form=PasswordChangeForm(request.user, request.POST) 
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            posts=Post.objects.filter(author=request.user, published_date__lte=timezone.now()).order_by('-published_date')
            return render(request, 'blog/user_detail.html', {'user': request.user, 'posts': posts})
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form=PasswordChangeForm(request.user)
    return render(request, 'blog/password_change.html', {'form': form})

@login_required
def user_edit(request):
    if request.method == 'POST':
        p_form=ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        u_form=UserUpdateForm(request.POST, instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            u_form.save()
            p_form.save()
            posts=Post.objects.filter(author=request.user, published_date__lte=timezone.now()).order_by('-published_date')
            messages.success(request,'Your Profile has been updated!')
            return render(request, 'blog/user_detail.html', {'user': request.user, 'posts': posts})
    else:
        p_form=ProfileForm(instance=request.user.profile)
        u_form=UserUpdateForm(instance=request.user)
    return render(request, 'blog/user_edit.html', {'u_form': u_form, 'p_form': p_form})

def SearchListView(request):
    
    word=request.GET.get('q')
    index=Index()
    index.create()
    posts=index.find(word)
    buffer_text=""
    if (word.strip()=='') or (len(word)>100) or (len(word)<3):
            buffer_text="Search text should be from 3 to 100 characters."
    elif len(posts)==0:
        buffer_text="Nothing found"

    if request.user.is_authenticated:
        new_not=Notification.objects.filter(subscriber=request.user, status=False).count()
        return render(request, 'blog/post_draft_list.html', {'posts': posts, 'buffer_text':buffer_text, 'notifications': Notification.objects.filter(subscriber=request.user).order_by('-pk'), 'new_not': new_not})
    else:
        return render(request, 'blog/post_draft_list.html', {'posts': posts, 'buffer_text':buffer_text, 'notifications': [], 'new_not': 0})



class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all().order_by('-date_joined')
    serializer_class=UserSerializer
    permission_classes=[permissions.IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    queryset=Post.objects.all().order_by('-created_date')
    serializer_class=PostSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
