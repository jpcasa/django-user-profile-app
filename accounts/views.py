from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from . import models
from . import forms

def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('home')  # TODO: go to profile
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('home'))  # TODO: go to profile
    return render(request, 'accounts/sign_up.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


def profile(request):
    """Display User Profile"""
    profile = request.user.profile
    return render(request, 'accounts/profile.html', {
        'profile': profile
    })


def edit_profile(request):
    user = request.user
    profile = get_object_or_404(models.Profile, user=user)
    form = forms.ProfileForm(instance=profile)

    if request.method == 'POST':
        form = forms.ProfileForm(instance=profile, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated the Profile Successfully!")
            return HttpResponseRedirect(reverse('accounts:profile'))

    return render(request, 'accounts/edit_profile.html', {
        'form': form
    })
