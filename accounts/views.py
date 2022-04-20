from email import message
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, update_session_auth_hash,login
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordChangeDoneView
from .forms import CreateUserForm, ProfileForm, UserEditForm


class MyLoginView(LoginView):
    template_name = 'registration/login.html'
    
def RegisterView(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.phone_no = form.cleaned_data.get('phone_no')
            user.profile.state = form.cleaned_data.get('state')
            user.save()

            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            # messages.add_message(request, messages.SUCCESS,
            #                      'Your profile was successfully updated!')
            return redirect('dashboard')
        
    else:
        form = CreateUserForm()

   
    # PAGE TITLE
    page_title = "Register"

    return render(request, 'registration/register.html', {
        'form': form,
        'page_title' : page_title,
    })


def ProfileView(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.warning(request, 'Please correct the error below.')
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        
    
        # PAGE TITLE
    page_title = "Profile Settings"

    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form' : profile_form,
        'page_title' : page_title,
    })
        
    