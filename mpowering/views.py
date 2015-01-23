
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from mpowering.forms import ResourceCreateForm
from mpowering.models import Tag, Resource, Organisation, ResourceURL , Category
from mpowering.models import ResourceFile, ResourceOrganisation, ResourceTag

from mpowering.signals import resource_viewed, resource_url_viewed, resource_file_viewed
# Create your views here.


def home_view(request):
    topics = Tag.objects.filter(category__slug='health-topic').order_by('order_by')
    return render_to_response('mpowering/home.html',
                              {'topics': topics,},
                              context_instance=RequestContext(request))

def tag_view(request,tag_slug):
    try:
        tag = Tag.objects.get(slug=tag_slug)
    except Tag.DoesNotExist:
        raise Http404()
    resources = Resource.objects.filter(resourcetag__tag=tag, status=Resource.APPROVED)
    return render_to_response('mpowering/tag.html',
                              {'resources': resources,
                               'tag': tag, },
                              context_instance=RequestContext(request))
  
def resource_view(request,resource_slug):
    try:
        resource = Resource.objects.get(slug=resource_slug)
    except Resource.DoesNotExist:
        raise Http404()
    
    if not resource_can_view(resource,request.user):
        raise Http404()
    
    if resource.status != Resource.APPROVED:
        messages.error(request, _(u"This resource is not yet approved by the mPowering Content Review Team, so is not yet available for all users to view"))
        
    resource_viewed.send(sender=resource, resource=resource, request=request)
    return render_to_response('mpowering/resource/view.html',
                              {'resource': resource, 
                               },
                              context_instance=RequestContext(request))  
    
def resource_create_view(request):
    if request.user.is_anonymous():
        return render_to_response('mpowering/login_required.html',
                              {'message': _(u'You need to be logged in to add a resource.') },
                              context_instance=RequestContext(request))
    if request.method == 'POST':
        form = ResourceCreateForm(request.POST, request.FILES)
        resource_form_set_choices(form)
        if form.is_valid():
            # save resource
            resource = Resource(status = Resource.PENDING, create_user = request.user, update_user = request.user)
            resource.title = form.cleaned_data.get("title")
            resource.description = form.cleaned_data.get("description")
            if request.FILES.has_key('image'):
                resource.image = request.FILES["image"]
            resource.save()
            
            # add organisation(s)
            organisations = [x.strip() for x in form.cleaned_data.get("organisations").split(',')]
            for o in organisations:
                try:
                    organisation = Organisation.objects.get(name = o)
                except Organisation.DoesNotExist:
                    organisation = Organisation(name =o, create_user=request.user, update_user=request.user).save()
                ResourceOrganisation(resource=resource, organisation=organisation,create_user=request.user).save()
                
            # add file and url
            if request.FILES.has_key('file'):
                rf = ResourceFile(resource=resource, create_user=request.user, update_user=request.user)
                rf.file=request.FILES["file"]
                rf.save()
                
            # add tags
            tag_categories = ["health_topic", "resource_type", "audience", "geography", "device"]
            for tc in tag_categories:
                tag_category = form.cleaned_data.get(tc)
                for ht in tag_category:
                    tag = Tag.objects.get(pk=ht)
                    ResourceTag(tag=tag, resource= resource, create_user= request.user).save()
                    
            # add license
            license = form.cleaned_data.get("license")
            tag = Tag.objects.get(pk=license)
            ResourceTag(tag=tag, resource= resource, create_user= request.user).save()
                    
            # add misc_tags
            other_tags = [x.strip() for x in form.cleaned_data.get("other_tags").split(',')]
            for ot in other_tags:
                if ot:
                    try:
                        tag = Tag.objects.get(name = ot)
                    except Tag.DoesNotExist:
                        category = Category.objects.get(slug='other')
                        tag = Tag(name =ot, category= category, create_user=request.user, update_user=request.user)
                        tag.save()
                    ResourceTag(tag=tag, resource= resource, create_user= request.user).save()
                
            # redirect to info page
            return HttpResponseRedirect(reverse('mpowering_resource_create_thanks', args=[resource.id])) # Redirect after POST
            
    else:
        form = ResourceCreateForm()
        resource_form_set_choices(form)
        
    return render_to_response('mpowering/resource/create.html',
                              {'form': form, 
                               },
                              context_instance=RequestContext(request))
 
def resource_create_thanks_view(request,id):
    resource = Resource.objects.get(pk=id)
    return render_to_response('mpowering/resource/create_thanks.html',
                              {'resource': resource, 
                               },
                              context_instance=RequestContext(request))
       
def resource_link_view(request, id):
    # TODO check that resource is approved
    try:
        url = ResourceURL.objects.get(pk=id)
        
        if not resource_can_view(url.resource,request.user):
            raise Http404() 
        
        resource_url_viewed.send(sender=url, resource_url=url, request=request)
        return HttpResponseRedirect(url.url)
    except ResourceURL.DoesNotExist:
        raise Http404()
    
def resource_file_view(request, id):
    # TODO check that resource is approved
    try:
        file = ResourceFile.objects.get(pk=id)
        
        if not resource_can_view(file.resource,request.user):
            raise Http404() 
        
        resource_file_viewed.send(sender=file, resource_file=file, request=request)
        response = HttpResponse(file.file, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = "attachment; filename=" + file.filename()
        return response
    except ResourceFile.DoesNotExist:
        raise Http404()
    
    
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

def resource_can_view(resource, user):
    if user.is_staff or user == resource.create_user or user == resource.update_user:
        return True
    elif resource.status == Resource.APPROVED:
        return True
    else:
        return False

def resource_can_edit(resource,user):
    if user.is_staff or user == resource.create_user or user == resource.update_user:
        return True
    else:
        return False