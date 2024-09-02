from friend.models import FriendList, FriendRequest
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.dispatch import receiver 
from django.contrib.auth.signals import user_logged_in, user_logged_out
from notification.models import Notification
import requests
from django.conf import settings
from friend.utils import get_friend_request_or_false
from friend.friend_request_status import FriendRequestStatus
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from .models import User 
from blog.models import Post
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from blog.models import Post
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@login_required(login_url='/admin_login/')
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('view_posts')
    return redirect('view_posts')

@login_required
def view_all_posts(request):
    posts = Post.objects.all()
    return render(request, 'users/admin_viewAllPosts.html', {'posts': posts})



def admin_logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    
    # Use reverse to dynamically generate the URL for the 'firsthome' view
    firsthome_url = reverse('firsthome')
    
    return redirect(firsthome_url)



User = get_user_model()

def changePassword(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    error = ""
    user = request.user
    
    if request.method == "POST":
        old_password = request.POST['oldpassword']
        new_password = request.POST['newpassword']
        
        try:
            user = User.objects.get(id=request.user.id)
            
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                error = "no"
                messages.success(request, 'Password updated successfully.Login again!!!')
                firsthome_url = reverse('firsthome')
                return redirect(firsthome_url)  # Redirect to logout after a successful password change
            else:
                error = 'not'
        except:
            error = "yes"

    return render(request, 'users/adminChangePassword.html', locals())

@login_required
def register_and_list_users(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Your account has been created! You can login now")
            return redirect('login')
    else:
        form = UserRegisterForm()

    users = User.objects.all()
    return render(request, 'users/register_and_list_users.html', {'form': form, 'users': users})

@login_required(login_url='/admin_login/')
def delete_blog_user(request, pid):
    try:
        user = User.objects.get(id=pid)  # Use 'id' to retrieve the user by primary key
        user.delete()
        # messages.success(request, "Delete Successful")
    except User.DoesNotExist:
        messages.error(request, "User not found")
    
    return redirect('register_and_list_users') 


def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pwd')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            # Assuming you have a user object, you can use login()
            login(request, user)
            total_users = User.objects.all().count()
            total_posts = Post.objects.all().count()
            return render(request, 'users/admin_home.html', {'total_users': total_users, 'total_posts': total_posts})  # Redirect to the admin home page after successful login
        else:
            # Handle invalid login credentials
            return render(request, 'users/adminlogin.html', {'error': 'yes'})

    return render(request, 'users/adminlogin.html')


def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    total_users = User.objects.all().count()
    total_posts = Post.objects.all().count()

    print("Total Users:", total_users)
    print("Total Posts:", total_posts)

    return render(request, 'users/admin_home.html', {'total_users': total_users, 'total_posts': total_posts})

@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):    
    user.profile.is_online = True
    user.profile.save()

@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):   
    user.profile.is_online = False
    user.profile.save()


""" Following and Unfollowing users """
@login_required
def follow_unfollow_profile(request):
    if request.method == 'POST':
        my_profile = Profile.objects.get(user = request.user)
        pk = request.POST.get('profile_pk')
        obj = Profile.objects.get(pk=pk)

        if obj.user in my_profile.following.all():
            my_profile.following.remove(obj.user)
            notify = Notification.objects.filter(sender=request.user, notification_type=2)
            notify.delete()
        else:
            my_profile.following.add(obj.user)
            notify = Notification(sender=request.user, user=obj.user, notification_type=2)
            notify.save()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile-list-view')




def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            
            # Check if the email is already registered
            if User.objects.filter(email=email).exists():
                messages.error(request, f"The email {email} is already registered. Please use a different email.")
                return render(request, 'users/register.html', {'form': form})

            # Save user registration
            user = form.save()
            
            # Send a welcome email
            subject = 'Welcome to BlogVista - Unleash Your Creativity! 🚀'
            html_content = render_to_string('users/welcome_email.html', {
                'user_first_name': user.first_name,
                'user_last_name': user.last_name,
                'user_username': user.username,
            })
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(subject, text_content, 'from@example.com', [user.email])
            email.attach_alternative(html_content, "text/html")
            email.send()

            messages.success(request, f"Your account has been created! A welcome email has been sent to {user.email}.")
            return redirect('login')
                
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

""" User profile """
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form':u_form,
        'p_form':p_form
    }

    return render(request, 'users/profile.html', context)


""" Creating a public profile view """
def public_profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'users/public_profile.html', {"cuser":user})


""" All user profiles """
class ProfileListView(LoginRequiredMixin,ListView):
    model = Profile
    template_name = "users/all_profiles.html"
    context_object_name = "profiles"

    def get_queryset(self):
        return Profile.objects.all().exclude(user=self.request.user)

""" User profile details view """
class ProfileDetailView(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = "users/user_profile_details.html"
    context_object_name = "profiles"

    def get_queryset(self):
        return Profile.objects.all().exclude(user=self.request.user)

    def get_object(self,**kwargs):
        pk = self.kwargs.get("pk")
        view_profile = Profile.objects.get(pk=pk)
        return view_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_profile = self.get_object()
        my_profile = Profile.objects.get(user=self.request.user)
        if view_profile.user in my_profile.following.all():
            follow = True
        else:
            follow = False
        context["follow"] = follow

        # FRIENDS START

        account = view_profile.user
        try:
            friend_list = FriendList.objects.get(user=account)
        except FriendList.DoesNotExist:
            friend_list = FriendList(user=account)
            friend_list.save()
        friends = friend_list.friends.all()
        context['friends']=friends

        is_self = True
        is_friend = False
        request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
        friend_requests = None
        user=self.request.user
        if user.is_authenticated and user!=account:
            is_self = False
            if friends.filter(pk=user.id):
                is_friend = True
            else:
                is_friend = False
                # CASE 1: request from them to you
                if get_friend_request_or_false(sender=account, receiver=user) != False:
                    request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                    context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).pk
                # CASE 2: request you sent to them
                elif get_friend_request_or_false(sender=user, receiver=account) != False:
                    request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
                # CASE 3: no request has been sent
                else:
                    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value

        elif not user.is_authenticated:
            is_self = False
        else:
            try:
                friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
            except:
                pass
        context['request_sent'] = request_sent
        context['is_friend'] = is_friend
        context['is_self'] = is_self
        context['friend_requests'] = friend_requests
        # FRIENDS END
        
        return context

