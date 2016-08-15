# orb/rating/views.py

from django.shortcuts import render


def country_map_view(request):
    return render(request, 'orb/viz/country_map.html')
