
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from mpowering.forms import ResourceCreateForm
from mpowering.models import Tag, Resource, Organisation, ResourceURL, ResourceFile

from mpowering.signals import resource_viewed, resource_url_viewed
# Create your views here.


def home_view(request):
    topics = Tag.objects.filter(category__slug='health-topic').order_by('order_by')
    return render_to_response('mpowering/home.html',
                              {'topics': topics,},
                              context_instance=RequestContext(request))

def tag_view(request,tag_slug):
    tag = Tag.objects.get(slug=tag_slug)
    resources = Resource.objects.filter(resourcetag__tag=tag, status=Resource.APPROVED)
    return render_to_response('mpowering/tag.html',
                              {'resources': resources,
                               'tag': tag, },
                              context_instance=RequestContext(request))
  
def resource_view(request,resource_slug):
    resource = Resource.objects.get(slug=resource_slug, status=Resource.APPROVED)
    resource_viewed.send(sender=resource, resource=resource, request=request)
    return render_to_response('mpowering/resource/view.html',
                              {'resource': resource, 
                               },
                              context_instance=RequestContext(request))  
    
def resource_create_view(request):
    if request.method == 'POST':
        form = ResourceCreateForm(request.POST, request.FILES)
        resource_form_set_choices(form)
        if form.is_valid():
            pass
    else:
        form = ResourceCreateForm()
        resource_form_set_choices(form)
        
    return render_to_response('mpowering/resource/create.html',
                              {'form': form, 
                               },
                              context_instance=RequestContext(request))
    
def resource_link_view(request, id):
    try:
        url = ResourceURL.objects.get(pk=id)
        resource_url_viewed.send(sender=url, resource_url=url, request=request)
        return HttpResponseRedirect(url.url)
    except ResourceURL.DoesNotExist:
        raise Http404()
    
def resource_file_view(request, id):
    return render_to_response('mpowering/resource/file.html',
                              context_instance=RequestContext(request))

def resource_form_set_choices(form):
    form.fields['health_topic'].choices = [(t.id, t.name) for t in Tag.objects.filter(category__slug='health-topic').order_by('order_by')]
    form.fields['resource_type'].choices = [(t.id, t.name) for t in Tag.objects.filter(category__slug='type').order_by('order_by')]
    form.fields['audience'].choices = [(t.id, t.name) for t in Tag.objects.filter(category__slug='audience').order_by('order_by')]
    form.fields['geography'].choices = [(t.id, t.name) for t in Tag.objects.filter(category__slug='geography').order_by('order_by')]
    form.fields['device'].choices = [(t.id, t.name) for t in Tag.objects.filter(category__slug='device').order_by('order_by')]
    form.fields['license'].choices = [(t.id, t.name) for t in Tag.objects.filter(category__slug='license').order_by('order_by')]
    return form 