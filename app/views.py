from django.shortcuts import render


def home(request):
    profile = request.user.profile
    return render(request, 'home.html', {
        'profile': profile
    })
