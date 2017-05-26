
from __future__ import unicode_literals

import json

from django import http
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.views.generic import ListView, UpdateView

from orb import mixins
from orb.courses import forms
from orb.courses import models


class CoursesListView(ListView):
    model = models.Course


@login_required
def course_list(request):
    return render(request, "orb/courses/course_list.html", {
        'courses': models.Course.courses.active(),
    })


@login_required
def course_create(request):
    return render(request, "orb/courses/course_form.html", {

    })


class CourseUpdateView(mixins.LoginRequiredMixin, UpdateView):
    """
    View for displaying and editing a course
    
    The GET method is based entirely on rendered template HTML
    
    The POST method is entirely AJAX/JSON based
    """
    queryset = models.Course.courses.active()
    fields = ['title', 'sections']
    template_name = "orb/courses/course_form.html"

    def user_can_edit(self, user):
        """Checks if the user has the right to edit this course"""
        return user.is_staff or user == self.object.create_user

    def get_context_data(self, **kwargs):
        context = super(CourseUpdateView, self).get_context_data(**kwargs)
        context.update({'can_edit': self.user_can_edit(self.request.user)})
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles a JSON request to save the course data
        
        Args:
            request: 
            *args: 
            **kwargs: 

        Returns:

        """
        if not self.user_can_edit(request.user):
            return http.JsonResponse({'errors': _('You do not have permission to edit this course')}, status=403)

        try:
            data = json.loads(request.content)
        except ValueError:
            return http.JsonResponse({'errors': _('JSON decoding error')}, status=400)

        form = forms.CourseForm(data=data)

        if form.is_valid():
            form.save()  # Any checks against resource keys should happen here
            return http.JsonResponse({'status': 'ok'})

        else:
            # form.errors is a dictionary with field names for keys and
            # the values of each is a list of errors in string format
            return http.JsonResponse({'errors': form.errors}, status=400)



