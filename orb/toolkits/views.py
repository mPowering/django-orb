# orb/toolkit/views.py

from django.shortcuts import render
from django.views.generic import ListView
from orb.toolkits.models import Toolkit


def toolkit_home_view(request):
    return render(request, 'orb/toolkits/home.html')


class ToolkitsView(ListView):
    """

    Args:
        request:

    Returns:

    """
    model = Toolkit
    template_name = "orb/toolkits/toolkit_list.html"
    context_object_name = "toolkits"
