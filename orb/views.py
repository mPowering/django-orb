# orb/views.py
import os 

from django.conf import settings
from django.contrib import messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.db.models import Count, Max, Min, Q
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import urlencode
from django.utils.translation import ugettext as _

from haystack.query import SearchQuerySet

from orb.forms import ResourceForm, SearchForm, TagFilterForm, ResourceRejectForm
from orb.models import Tag, Resource, ResourceURL , Category, TagOwner
from orb.models import ResourceFile, ResourceTag, ResourceWorkflowTracker, ResourceCriteria
from orb.signals import resource_viewed, resource_url_viewed, resource_file_viewed, search, resource_workflow

from PIL import Image


def home_view(request):
    topics = []
    tags = Tag.objects.filter(category__top_level=True, parent_tag=None).order_by('order_by')
    for t in tags:
       # get child tags
       child_tags = Tag.objects.filter(parent_tag=t).values_list('id')
       
       resource_count = Resource.objects.filter(status=Resource.APPROVED).filter(Q(resourcetag__tag__pk__in=child_tags) | Q(resourcetag__tag=t)).distinct().count()
       data = {}
       data['resource_count']= resource_count
       data['tag'] = t
       topics.append(data)
    
    return render_to_response('orb/home.html',
                              {'topics': topics,},
                              context_instance=RequestContext(request))


def partner_view(request):
    partners = Tag.objects.filter(category__slug='organisation').exclude(description=None).exclude(description="").order_by('name')
    return render_to_response('orb/partners.html',
                              {'partners': partners,},
                              context_instance=RequestContext(request))
    
def tag_view(request,tag_slug):
    
    tag = get_object_or_404(Tag, slug=tag_slug)
    child_tags = Tag.objects.filter(parent_tag=tag, resourcetag__resource__status=Resource.APPROVED).annotate(resource_count=Count('resourcetag__resource')).order_by('order_by')
    
    CREATED = u'-create_date'
    TITLE = u'title'
    ORDER_OPTIONS = (
        (CREATED, _(u'Create date')),
        (TITLE, _(u'Title')),
    )
    
    order_by = request.GET.get('order', CREATED)
    
    data = Resource.objects.filter(resourcetag__tag=tag, status=Resource.APPROVED).order_by(order_by)
    
    paginator = Paginator(data, 20)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        resources = paginator.page(page)
    except (EmptyPage, InvalidPage):
        resources = paginator.page(paginator.num_pages)
    
    show_filter_link = False
    if tag.category.slug in [slug for name, slug in settings.TAG_FILTER_CATEGORIES]:
        show_filter_link = True
        
    return render_to_response('orb/tag.html',
                              {
                               'tag': tag,
                               'child_tags': child_tags, 
                               'page':resources,
                               'ordering': ORDER_OPTIONS, 
                               'current_order': order_by,
                               'show_filter_link': show_filter_link,
                               },
                              context_instance=RequestContext(request))

def tag_cloud_view(request):
    
    tags = Tag.objects.filter(resourcetag__resource__status=Resource.APPROVED).annotate(dcount=Count('resourcetag__resource')).order_by('name')
    max = tags.aggregate(max=Max('dcount'))
    min = tags.aggregate(min=Min('dcount'))
    diff = max['max']-min['min']
    return render_to_response('orb/tag_cloud.html',
                              { 'tags': tags,
                               'diff': diff
                               },
                              context_instance=RequestContext(request))

def tag_filter_view(request, tag_id=None):

    if request.method == 'POST':
        form = TagFilterForm(request.POST)
        tag_filter_form_set_choices(form)
        if form.is_valid():
            urlparams = request.POST.copy()
            # delete these from params as not required
            del urlparams['csrfmiddlewaretoken']
            del urlparams['submit']
            return HttpResponseRedirect(reverse('orb_tags_filter_results') + "?" + urlparams.urlencode())
    else:
        data = {}
        if tag_id:
            tag = get_object_or_404(Tag, pk=tag_id)
            for name, slug in settings.TAG_FILTER_CATEGORIES:
                if tag.category.slug == slug:
                    data[name] = tag.id
        form = TagFilterForm(initial=data)
        tag_filter_form_set_choices(form)
     
    return render_to_response('orb/tag_filter.html',
                              {'form': form,
                               },
                              context_instance=RequestContext(request))
       
def tag_filter_results_view(request): 
    form = TagFilterForm(request.GET)
    tag_filter_form_set_choices(form)
    if form.is_valid():
        tag_ids = []
        for name, slug  in settings.TAG_FILTER_CATEGORIES:
            for i in form.cleaned_data.get(name):
                tag_ids.append(i)
        resource_tags = ResourceTag.objects.filter(tag__pk__in=tag_ids).values('resource').annotate(dcount=Count('resource')).filter(dcount=len(tag_ids)).values('resource')
        
        data = Resource.objects.filter(pk__in=resource_tags, status=Resource.APPROVED)
        
        paginator = Paginator(data, 20)
        # Make sure page request is an int. If not, deliver first page.
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        
        try:
            resources = paginator.page(page)
        except (EmptyPage, InvalidPage):
            resources = paginator.page(paginator.num_pages)
        
        filter_tags = Tag.objects.filter(pk__in=tag_ids)
    return render_to_response('orb/tag_filter_results.html',
                              { 'filter_tags': filter_tags,
                               'page':resources,},
                              context_instance=RequestContext(request))

def taxonomy_view(request):
    return render_to_response('orb/taxonomy.html',
                              { },
                              context_instance=RequestContext(request))
    
def resource_permalink_view(request,id):
    try:
        resource = Resource.objects.get(pk=id)
    except Resource.DoesNotExist:
        raise Http404()
    
    return resource_view(request, resource.slug)
  
def resource_view(request,resource_slug):
    try:
        resource = Resource.objects.get(slug=resource_slug)
    except Resource.DoesNotExist:
        raise Http404()
    
    if not resource_can_view(resource,request.user):
        raise Http404()
    
    if resource.status != Resource.APPROVED:
        messages.error(request, _(u"This resource is not yet approved by the ORB Content Review Team, so is not yet available for all users to view"))
    
    options_menu = []
    if resource_can_edit(resource,request.user):
        om = {}
        om['title'] = _(u'Edit')   
        om['url'] = reverse('orb_resource_edit', args=[resource.id])
        options_menu.append(om)
    
    if request.user.is_staff:
        if resource.status==Resource.PENDING_CRT:
            om = {}
            om['title'] = _(u'Send to MEP')   
            om['url'] = reverse('orb_resource_pending_mep', args=[resource.id])
            options_menu.append(om)
        if resource.status == Resource.PENDING_CRT or resource.status == Resource.PENDING_MRT:   
            om = {}
            om['title'] = _(u'Reject')   
            om['url'] = reverse('orb_resource_reject', args=[resource.id])
            options_menu.append(om)
            
            om = {}
            om['title'] = _(u'Approve')   
            om['url'] = reverse('orb_resource_approve', args=[resource.id])
            options_menu.append(om)

    resource_viewed.send(sender=resource, resource=resource, request=request)
    return render_to_response('orb/resource/view.html',
                              {'resource': resource, 
                               'options_menu': options_menu, },
                              context_instance=RequestContext(request))  
    
def resource_create_view(request):
    if request.user.is_anonymous():
        return render_to_response('orb/login_required.html',
                              {'message': _(u'You need to be logged in to add a resource.') },
                              context_instance=RequestContext(request))
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        resource_form_set_choices(form)
        if form.is_valid():
            # save resource
            resource = Resource(status = Resource.PENDING_CRT, create_user = request.user, update_user = request.user)
            resource.title = form.cleaned_data.get("title")
            resource.description = form.cleaned_data.get("description")
            if form.cleaned_data.get("study_time_number") and form.cleaned_data.get("study_time_unit"):
                resource.study_time_number = form.cleaned_data.get("study_time_number")
                resource.study_time_unit = form.cleaned_data.get("study_time_unit")
            if request.FILES.has_key('image'):
                resource.image = request.FILES["image"]
            resource.save()
            
            # add organisation(s)/geography and other tags
            resource_add_free_text_tags(request, form, resource, 'organisations','organisation')
            resource_add_free_text_tags(request, form, resource, 'geography','geography')
            resource_add_free_text_tags(request, form, resource, 'languages','language')
            resource_add_free_text_tags(request, form, resource, 'other_tags','other')
                
            # add file and url
            if request.FILES.has_key('file'):
                rf = ResourceFile(resource=resource, create_user=request.user, update_user=request.user)
                rf.file=request.FILES["file"]
                rf.save()
            
            url = form.cleaned_data.get("url")
            if url:
                ru = ResourceURL(resource=resource, create_user=request.user, update_user=request.user) 
                ru.url = url
                ru.save()
                
            # add tags
            resource_add_tags(request, form, resource)
              
            # see if email needs to be sent
            resource_workflow.send(sender=resource, resource=resource, request=request, status=ResourceWorkflowTracker.PENDING_CRT, notes="")  
            
            # redirect to info page
            return HttpResponseRedirect(reverse('orb_resource_create_thanks', args=[resource.id])) # Redirect after POST
            
    else:
        user_org = request.user.userprofile.organisation.name
        form = ResourceForm(initial={'organisations':user_org,})
        resource_form_set_choices(form)
        
    return render_to_response('orb/resource/create.html',
                              {'form': form, 
                               },
                              context_instance=RequestContext(request))
 
def resource_create_thanks_view(request,id):
    try:
        resource = Resource.objects.get(pk=id)
    except Resource.DoesNotExist:
        raise Http404()
    if not resource_can_edit(resource, request.user):
        raise Http404()
    return render_to_response('orb/resource/create_thanks.html',
                              {'resource': resource, 
                               },
                              context_instance=RequestContext(request))
    
def resource_guidelines_view(request):
    
    criteria = []
    
    resource_criteria = ResourceCriteria.objects.all().order_by('category_order_by', 'order_by')
    
    return render_to_response('orb/resource/guidelines.html',
                              {'criteria': criteria, 
                               },
                              context_instance=RequestContext(request))
    
def resource_approve_view(request, id):
    if not request.user.is_staff:
        return HttpResponse(status=401,content="Not Authorized") 
    resource = Resource.objects.get(pk=id)
    resource.status = Resource.APPROVED
    resource.save()
    
    resource_workflow.send(sender=resource, resource=resource, request=request, status=ResourceWorkflowTracker.APPROVED, notes="")
    return render_to_response('orb/resource/status_updated.html',
                              { 'resource':resource,},
                              context_instance=RequestContext(request))
    
def resource_reject_view(request, id):
    if not request.user.is_staff:
        return HttpResponse(status=401,content="Not Authorized")
    
    resource = Resource.objects.get(pk=id)
    
    if request.method == 'POST':
        form = ResourceRejectForm(data = request.POST)
            
        if form.is_valid():
            resource.status = Resource.REJECTED
            resource.save()
            notes = form.cleaned_data.get("notes")
            resource_workflow.send(sender=resource, resource=resource, request=request, status=ResourceWorkflowTracker.REJECTED, notes=notes)
            return HttpResponseRedirect(reverse('orb_resource_reject_sent', args=[resource.id]))
    else:
        form = ResourceRejectForm()
        
    return render_to_response('orb/resource/reject_form.html',
                              { 'resource':resource,
                                'form': form },
                              context_instance=RequestContext(request))
    
def resource_reject_sent_view(request, id):
    if not request.user.is_staff:
        return HttpResponse(status=401,content="Not Authorized") 
    
    resource = Resource.objects.get(pk=id)
    
    return render_to_response('orb/resource/status_updated.html',
                              { 'resource':resource,},
                              context_instance=RequestContext(request))
    
def resource_pending_mep_view(request, id):
    if not request.user.is_staff:
        return HttpResponse(status=401,content="Not Authorized")
   
    resource = Resource.objects.get(pk=id)
    resource.status = Resource.PENDING_MRT
    resource.save()
    
    resource_workflow.send(sender=resource, resource=resource, request=request, status=ResourceWorkflowTracker.PENDING_MEP, notes="")
    return render_to_response('orb/resource/status_updated.html',
                              { 'resource':resource,},
                              context_instance=RequestContext(request))
    
    
def resource_link_view(request, id):
    try:
        url = ResourceURL.objects.get(pk=id)
        
        if not resource_can_view(url.resource,request.user):
            raise Http404() 
        
        resource_url_viewed.send(sender=url, resource_url=url, request=request)
        return HttpResponseRedirect(url.url)
    except ResourceURL.DoesNotExist:
        raise Http404()
    
def resource_file_view(request, id):
    try:
        file = ResourceFile.objects.get(pk=id)
        
        if not resource_can_view(file.resource,request.user):
            raise Http404() 
        
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, file.file.name)):
            resource_file_viewed.send(sender=file, resource_file=file, request=request)
            response = HttpResponse(file.file, content_type='application/unknown;charset=utf-8')
            response['Content-Disposition'] = "attachment; filename=" + file.filename()
            return response
        else:
           raise Http404() 
    except ResourceFile.DoesNotExist:
        raise Http404()
    
    
    return render_to_response('orb/resource/file.html',
                              context_instance=RequestContext(request))

def resource_edit_view(request,resource_id):
    resource = Resource.objects.get(pk=resource_id)
    if not resource_can_edit(resource, request.user):
        raise Http404() 

    if request.method == 'POST':
        form = ResourceForm(data = request.POST, files = request.FILES)
        resource_form_set_choices(form)
            
        if form.is_valid():
            resource.update_user = request.user
            resource.title = form.cleaned_data.get("title")
            resource.description = form.cleaned_data.get("description")
            if form.cleaned_data.get("study_time_number") and form.cleaned_data.get("study_time_unit"):
                resource.study_time_number = form.cleaned_data.get("study_time_number")
                resource.study_time_unit = form.cleaned_data.get("study_time_unit")
            resource.save()
                
            # update image
            image_clear = form.cleaned_data.get("image-clear")
        
            if image_clear:
                resource.image = None
                resource.save()
            
            if request.FILES.has_key('image'):
                resource.image = request.FILES["image"]
                resource.save()
            
            # update file
            file_clear = form.cleaned_data.get("file-clear")
            if file_clear:
                ResourceFile.objects.filter(resource=resource).delete()
                
            if request.FILES.has_key('file'):
                rf = ResourceFile(resource=resource, create_user=request.user, update_user=request.user)
                rf.file=request.FILES["file"]
                rf.save()   
            
            
            # update url
            url = form.cleaned_data.get("url")
            # check if resource already had a url or not
            urls = ResourceURL.objects.filter(resource=resource)
            if url:
                if urls:
                    resource_url = urls[0]
                    resource_url.url = url
                    resource_url.update_user = request.user
                    resource_url.save()
                else:
                    resource_url = ResourceURL(resource=resource, create_user=request.user, update_user=request.user) 
                    resource_url.url = url
                    resource_url.save()
            else:
                if urls:
                    urls.delete()
            
            
            # update tags - remove all current tags first
            ResourceTag.objects.filter(resource=resource).delete()
            resource_add_tags(request, form, resource)
            resource_add_free_text_tags(request, form, resource,'organisations','organisation')
            resource_add_free_text_tags(request, form, resource,'geography','geography')
            resource_add_free_text_tags(request, form, resource, 'languages','language')
            resource_add_free_text_tags(request, form, resource,'other_tags','other')
            
            # All successful - now redirect
            return HttpResponseRedirect(reverse('orb_resource_edit_thanks', args=[resource.id]))
        else:
            initial = request.POST
            initial['image'] = resource.image
            files = ResourceFile.objects.filter(resource=resource)[:1]
            if files:
                initial['file'] = files[0].file
            form = ResourceForm(initial = initial, data = request.POST, files = request.FILES)
            resource_form_set_choices(form)       
            
            
    else:
        data = {}
        data['title'] = resource.title
        organisations = Tag.objects.filter(category__slug='organisation',resourcetag__resource=resource).values_list('name', flat=True)
        data['organisations'] = ', '.join(organisations)
        data['description'] = resource.description
        data['image'] = resource.image
        data['study_time_number'] = resource.study_time_number
        data['study_time_unit'] = resource.study_time_unit
        
        files = ResourceFile.objects.filter(resource=resource)[:1]
        if files:
            data['file'] = files[0].file
        
        urls = ResourceURL.objects.filter(resource=resource)[:1]
        if urls:
            data['url'] = urls[0].url
            
        health_topic = Tag.objects.filter(category__top_level=True, resourcetag__resource=resource).values_list('id',flat=True)
        data['health_topic'] = health_topic
       
         
        resource_type = Tag.objects.filter(category__slug='type', resourcetag__resource=resource).values_list('id',flat=True)
        data['resource_type'] = resource_type
        
        audience = Tag.objects.filter(category__slug='audience', resourcetag__resource=resource).values_list('id',flat=True)
        data['audience'] = audience
        
        geography = Tag.objects.filter(category__slug='geography', resourcetag__resource=resource).values_list('name',flat=True)
        data['geography'] = ', '.join(geography)
        
        languages = Tag.objects.filter(category__slug='language', resourcetag__resource=resource).values_list('name',flat=True)
        data['languages'] = ', '.join(languages)
        
        device = Tag.objects.filter(category__slug='device', resourcetag__resource=resource).values_list('id',flat=True)
        data['device'] = device
        
        license = Tag.objects.filter(category__slug='license', resourcetag__resource=resource).values_list('id',flat=True)
        if license:
            data['license'] = license[0]
        
        other_tags = Tag.objects.filter(resourcetag__resource=resource, category__slug='other').values_list('name', flat=True)
        data['other_tags'] = ', '.join(other_tags)
        
        form = ResourceForm(initial= data)
        resource_form_set_choices(form )
        
    return render_to_response('orb/resource/edit.html',
                              {'form': form, 
                               },
                              context_instance=RequestContext(request))
    
def resource_edit_thanks_view(request,id):
    try:
        resource = Resource.objects.get(pk=id)
    except Resource.DoesNotExist:
        raise Http404()
    if not resource_can_edit(resource, request.user):
        raise Http404()
    return render_to_response('orb/resource/edit_thanks.html',
                              {'resource': resource, 
                               },
                              context_instance=RequestContext(request))

def resource_rate_view(request):
    if request.user.is_anonymous():
        raise Http404()
    if request.method == 'POST':
        resource_id = request.POST.get('resource_id')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        return HttpResponse()
    else:
        raise Http404()   
    

def search_view(request):
     
    search_query = request.GET.get('q', '')
    
    if search_query:
        search_results = SearchQuerySet().filter(content=search_query)
        search.send(sender=search_results, query=search_query, no_results=search_results.count(), request=request)
    else:
        search_results = []
        
    data = {}
    data['q'] = search_query
    form = SearchForm(initial=data)
     
     
    paginator = Paginator(search_results, 20)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        results = paginator.page(page)
    except (EmptyPage, InvalidPage):
        results = paginator.page(paginator.num_pages)
           
    return render_to_response('orb/search.html',
                              {'form': form, 
                               'query': search_query,
                               'page': results},
                              context_instance=RequestContext(request))
    


''' 
Helper functions
'''
def resource_form_set_choices(form):
    form.fields['health_topic'].choices = [(t.id, t.name) for t in Tag.objects.filter(category__top_level=True).order_by('order_by','name')]
    form.fields['resource_type'].choices = [(t.id, t.name) for t in Tag.objects.filter(category__slug='type').order_by('order_by','name')]
    form.fields['audience'].choices = [(t.id, t.name) for t in Tag.objects.filter(category__slug='audience').order_by('order_by','name')]
    form.fields['device'].choices = [(t.id, t.name) for t in Tag.objects.filter(category__slug='device').order_by('order_by','name')]
    form.fields['license'].choices = [(t.id, t.name) for t in Tag.objects.filter(category__slug='license').order_by('order_by','name')]
    return form 

def tag_filter_form_set_choices(form):
    for name, slug in settings.TAG_FILTER_CATEGORIES:
        form.fields[name].choices = [(t.id, t.name) for t in Tag.objects.filter(category__slug=slug).exclude(resourcetag__isnull=True).order_by('order_by','name')]
    return form 

def resource_can_view(resource, user):
    if user.is_staff or user == resource.create_user or user == resource.update_user:
        return True
    elif resource.status == Resource.APPROVED:
        return True
    else:
        print resource
        print user
        return False

def resource_can_edit(resource,user):
    if user.is_staff or user == resource.create_user or user == resource.update_user:
        return True
    else:
        tag_owner = TagOwner.objects.filter(user__pk=user.id,tag__resourcetag__resource=resource).count()
        if tag_owner > 0:
            return True
        else:
            return False

def resource_add_free_text_tags(request, form, resource, field, slug):
    free_text_tags = [x.strip() for x in form.cleaned_data.get(field).split(',')]
    for ftt in free_text_tags:
        if ftt != '':
            try:
                tag = Tag.objects.get(name = ftt, category__slug=slug)
            except Tag.DoesNotExist:
                category = Category.objects.get(slug=slug)
                tag = Tag(name=ftt, category= category, create_user=request.user, update_user=request.user)
                tag.save()
            try:
                ResourceTag(tag=tag, resource= resource, create_user= request.user).save()
            except IntegrityError:
                pass
                  
def resource_add_tags(request, form, resource):
    tag_categories = ["health_topic", "resource_type", "audience", "device"]
    for tc in tag_categories:
        tag_category = form.cleaned_data.get(tc)
        for ht in tag_category:
            tag = Tag.objects.get(pk=ht)
            ResourceTag(tag=tag, resource=resource, create_user=request.user).save()
    # add license
    license = form.cleaned_data.get("license")
    tag = Tag.objects.get(pk=license)
    ResourceTag(tag=tag, resource= resource, create_user= request.user).save()