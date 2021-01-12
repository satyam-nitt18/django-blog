from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment, Profile, Index
from .forms import PostForm, CommentForm, SignUpForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.views import generic
from .tokens import account_activation_token

# Create your views here.
def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post=get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post, 'is_user_liked': post.likes.filter(id=request.user.id).exists()})

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
    return render(request, 'blog/post_edit.html', {'form': form})

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
    return render(request, 'blog/post_edit.html', {'form':form})

@login_required
def post_draft_list(request):
    posts=Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

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

def add_comment_to_post(request, pk):
    post=get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid() :
            comment = form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

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
    #try:
    #    profile = request.user.profile
    #except Profile.DoesNotExist:
    #    profile = Profile(user=request.user)

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
    return render(request, 'registration/signup.html', {'form': form})

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
    
    return render(request, 'blog/post_draft_list.html', {'posts': posts, 'buffer_text':buffer_text})

'''
class SearchListView(generic.ListView):
    model=Post
    context_object_name='posts'
    template_name='blog/post_draft_list.html'

    def get_context_data(self, **kwargs):
        context=super(SearchListView, self).get_context_data()
        word=self.request.GET.get('q')
        context['search_text']=word

        if (len(word)<1) or (len(word)>100):
            context['text']="Search text should be from 3 to 100 characters."
        else:
            posts=Index.find(word)
            if posts:
                context['posts']=posts 
                context['query']=word
            else:
                context['text']="Nothing found"
        return context
'''