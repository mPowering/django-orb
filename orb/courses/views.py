from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView, UpdateView
from django.http import JsonResponse

from orb.courses.models import Course
from orb.mixins import LoginRequiredMixin


class CoursesListView(ListView):
    model = Course


@login_required
def course_list(request):
    return render(request, "orb/courses/course_list.html", {
        'courses': Course.courses.active(),
    })


@login_required
def course_create(request):
    return render(request, "orb/courses/course_form.html", {

    })


class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    fields = ['title', 'sections']
    template_name = "orb/courses/course_form.html"

    def post(self, request, *args, **kwargs):
        """
        Handles a JSON request
        
        Args:
            request: 
            *args: 
            **kwargs: 

        Returns:

        """
        return JsonResponse({})

