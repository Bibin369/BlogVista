from django.urls import path
from . import views
from .views import admin_login_view
from .views import admin_home
from .views import register_and_list_users
from .views import admin_logout_view
from .views import delete_blog_user,changePassword


urlpatterns = [
    path('all/', views.ProfileListView.as_view(), name='profile-list-view'),
    path('follow/', views.follow_unfollow_profile, name='follow-unfollow-view'),
    path('<int:pk>/', views.ProfileDetailView.as_view(), name='profile-detail-view'),
    path('public-profile/<str:username>/', views.public_profile, name='public-profile'),
    path('admin/login/', admin_login_view, name='admin_login'),
    path('admin/home/', admin_home, name='admin_home'),
    path('register/', register_and_list_users, name='register_and_list_users'),
    path('admin/logout/', admin_logout_view, name='admin_logout'),
    path('delete-user/<int:pid>/', delete_blog_user, name='delete_blog_user'),
    path('change-password/', changePassword, name='change_password'),
    path('delete_post/<int:pk>/', views.delete_post, name='delete_post'),
    path('view-posts/', views.view_all_posts, name='view_posts'),


]