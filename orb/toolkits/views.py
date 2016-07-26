# orb/toolkit/views.py

from django.shortcuts import render


def toolkit_home_view(request):
    return render(request, 'orb/toolkits/home.html')
