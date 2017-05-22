from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView, UpdateView

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

