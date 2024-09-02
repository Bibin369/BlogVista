from django.urls import path
from . import views
from .views import AllSaveView, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, SaveView, UserPostListView, LikeView,LikeCommentView, posts_of_following_profiles,  AllLikeView
from .views import contact_us
from .views import contact_us_details,manage_updates,delete_update

urlpatterns = [

    # urls.py
    path('contact-us/', contact_us, name='contact_us'),
    path('', views.first, name='firsthome'),
    path('home/', PostListView.as_view(), name='blog-home'),
    path('feed/', posts_of_following_profiles, name='posts-follow-view'),
    path('post/user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView, name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/like/', LikeView, name='post-like'),
    path('liked-posts/', AllLikeView, name='all-like'),
    path('post/save/', SaveView, name='post-save'),
    path('saved-posts/', AllSaveView, name='all-save'),
    path('post/comment/like/', LikeCommentView, name='comment-like'),
    path('about/', views.about, name='blog-about'),
    path('search/', views.search, name='search'),
    path('contact_us_details/', contact_us_details, name='contact_us_details'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('send-update/', views.send_update, name='send_update'),
    path('manage_updates/', manage_updates, name='manage_updates'),
    path('delete_update/<int:update_id>/', delete_update, name='delete_update'),
]