from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('post/<int:pk>/like/', views.PostLike, name='post_like'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('signup/', views.signup, name='signup'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),
    path('search/', views.SearchListView, name='search_results'),
    path('subscribe/', views.SubscribeOnBlogNotificationsView, name='subscribe'),
    path('unsubscribe/', views.UnsubscribeOnBlogNotificationsView, name='unsubscribe'),
    path('notification_delete/<int:pk>/', views.NotificationDeleteView, name='notification_delete'),
    path('user_detail/(?P<username>[\w.@+-]+)/', views.user_detail, name='user_detail'),
    path('password_change/', views.password_change, name='password_change'),
    path('user_edit/', views.user_edit, name='user_edit'),
    

]