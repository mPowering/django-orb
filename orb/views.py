# orb/views.py
import os 

from django.conf import settings
from django.contrib import messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.db.models import Count, Max, Min, Q, Avg
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import urlencode
from django.utils.translation import ugettext as _

from haystack.query import SearchQuerySet

from orb.forms import ResourceStep1Form, ResourceStep2Form, SearchForm, ResourceRejectForm, AdvancedSearchForm
from orb.models import Tag, Resource, ResourceURL , Category, TagOwner, TagTracker, SearchTracker
from orb.models import ResourceFile, ResourceTag, ResourceWorkflowTracker, ResourceCriteria, ResourceRating
from orb.models import Collection, CollectionResource, CollectionUser
from orb.signals import resource_viewed, resource_url_viewed, resource_file_viewed, search, resource_workflow, resource_submitted, tag_viewed

from PIL import Image

from orb.partners.OnemCHW.models import CountryData

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
                              {'topics': topics,
                               'page_title': _(u'ORB by mPowering')},
                              context_instance=RequestContext(request))


def partner_view(request):
    PARTNERS = ['jhu-ccp','digital-campus','digital-green','global-health-media-project', 'medical-aid-films', 'zinc-ors']
    partners = Tag.objects.filter(category__slug='organisation', slug__in=PARTNERS).order_by('name')
    return render_to_response('orb/partners.html',
                              {'partners': partners,},
                              context_instance=RequestContext(request))
    
def tag_view(request,tag_slug):
    
    tag = get_object_or_404(Tag, slug=tag_slug)
    child_tags = Tag.objects.filter(parent_tag=tag, resourcetag__resource__status=Resource.APPROVED).annotate(resource_count=Count('resourcetag__resource')).order_by('order_by','name')
    
    CREATED = u'-create_date'
    TITLE = u'title'
    UPDATED = u'-update_date'
    RATING = u'-rating'
    ORDER_OPTIONS = (
        (CREATED, _(u'Create date')),
        (TITLE, _(u'Title')),
        (RATING, _(u'Rating')),
        (UPDATED, _(u'Update date')),
    )
    
    order_by = request.GET.get('order', CREATED)
    
    if order_by == RATING:
        data = []
        data_top = Resource.objects.filter(resourcetag__tag=tag, status=Resource.APPROVED).annotate(rating=Avg('resourcerating__rating'),rate_count=Count('resourcerating')).exclude(rate_count__lt=settings.ORB_RESOURCE_MIN_RATINGS).order_by(order_by)
        for d in data_top:
            data.append(d)
            
        data_bottom = Resource.objects.filter(resourcetag__tag=tag, status=Resource.APPROVED).annotate(rating=Avg('resourcerating__rating'),rate_count=Count('resourcerating')).exclude(rate_count__gte=settings.ORB_RESOURCE_MIN_RATINGS).order_by(order_by)
        for d in data_bottom:
            data.append(d)
    else:
        data = Resource.objects.filter(resourcetag__tag=tag, status=Resource.APPROVED).order_by(order_by)
        
    paginator = Paginator(data, settings.ORB_PAGINATOR_DEFAULT)
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
    if tag.category.slug in [slug for name, slug in settings.ADVANCED_SEARCH_CATEGORIES]:
        show_filter_link = True
      
    tag_viewed.send(sender=tag, tag=tag, request=request)
      
    country_key_facts = None
    
    if settings.ORB_PARTNER_DATA_ENABLED:
        try:
            country_key_facts = CountryData.objects.get(slug=tag.slug)
        except CountryData.DoesNotExist:
            pass
        
    return render_to_response('orb/tag.html',
                              {
                               'tag': tag,
                               'child_tags': child_tags, 
                               'page':resources,
                               'ordering': ORDER_OPTIONS, 
                               'current_order': order_by,
                               'show_filter_link': show_filter_link,
                               'country_key_facts': country_key_facts,
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
    
    user_rating = 0
    if request.user.is_authenticated():
        try:
            user_rating = ResourceRating.objects.get(resource=resource,user=request.user).rating
        except ResourceRating.DoesNotExist:
            pass
    
    # get the collections for this resource
    collections = Collection.objects.filter(collectionresource__resource=resource, visibility=Collection.PUBLIC)
        
    # See if bookmarked
    bookmarks = Collection.objects.filter(collectionresource__resource=resource, visibility=Collection.PRIVATE, collectionuser__user__id=request.user.id).count()
    if bookmarks > 0:
        bookmarked = True
    else:
        bookmarked = False
        
    return render_to_response('orb/resource/view.html',
                              {'resource': resource, 
                               'options_menu': options_menu, 
                               'user_rating': user_rating,
                               'collections': collections,
                               'bookmarked': bookmarked },
                              context_instance=RequestContext(request))  
    
def resource_create_step1_view(request):
    if request.user.is_anonymous():
        return render_to_response('orb/login_required.html',
                              {'message': _(u'You need to be logged in to add a resource.') },
                              context_instance=RequestContext(request))
    if request.method == 'POST':
        form = ResourceStep1Form(request.POST, request.FILES, request=request)
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
            resource.attribution = form.cleaned_data.get("attribution")
            resource.save()
            
            # add organisation(s)/geography and other tags
            resource_add_free_text_tags(request, form, resource, 'organisations','organisation')
            resource_add_free_text_tags(request, form, resource, 'geography','geography')
            resource_add_free_text_tags(request, form, resource, 'languages','language')
            resource_add_free_text_tags(request, form, resource, 'other_tags','other')
                
            # add tags
            resource_add_tags(request, form, resource)
              
            # see if email needs to be sent
            resource_workflow.send(sender=resource, resource=resource, request=request, status=ResourceWorkflowTracker.PENDING_CRT, notes="")  
            resource_submitted.send(sender=resource, resource=resource, request=request)
            
            # redirect to step 2
            return HttpResponseRedirect(reverse('orb_resource_create2', args=[resource.id])) # Redirect after POST
            
    else:
        if request.user.userprofile.organisation:
            user_org = request.user.userprofile.organisation.name
            initial = {'organisations':user_org,}
        else:
            initial = {}
        form = ResourceStep1Form(initial=initial, request=request)
        resource_form_set_choices(form)
        
    return render_to_response('orb/resource/create_step1.html',
                              {'form': form, 
                               },
                              context_instance=RequestContext(request))
 
 
def resource_create_step2_view(request, id):
    if request.user.is_anonymous():
        return render_to_response('orb/login_required.html',
                              {'message': _(u'You need to be logged in to add a resource.') },
                              context_instance=RequestContext(request))
     
    try:
        resource = Resource.objects.get(pk=id)
    except Resource.DoesNotExist:
        raise Http404()
       
    # check if owner of this resource
    if not resource_can_edit(resource, request.user):
        raise Http404()
    
    if request.method == 'POST':
        form = ResourceStep2Form(request.POST, request.FILES, request=request)
        
        if form.is_valid():
            title = form.cleaned_data.get("title")
            # add file and url
            if request.FILES.has_key('file'):
                rf = ResourceFile(resource=resource, create_user=request.user, update_user=request.user)
                rf.file=request.FILES["file"]
                if title:
                    rf.title = title
                rf.save()
            
            url = form.cleaned_data.get("url")
            if url:
                ru = ResourceURL(resource=resource, create_user=request.user, update_user=request.user) 
                ru.url = url
                if title:
                    ru.title = title
                ru.save()
        
    initial = {}
    form = ResourceStep2Form(initial=initial, request=request)
       
    resource_files = ResourceFile.objects.filter(resource=resource)
    resource_urls = ResourceURL.objects.filter(resource=resource)
    
    return render_to_response('orb/resource/create_step2.html',
                              {'form': form, 
                               'resource': resource,
                               'resource_files': resource_files,
                               'resource_urls': resource_urls,
                               },
                              context_instance=RequestContext(request))

def resource_create_file_delete_view(request, id, file_id):
    # check ownership
    try:
        resource = Resource.objects.get(pk=id)
    except Resource.DoesNotExist:
        raise Http404()
    if not resource_can_edit(resource, request.user):
        raise Http404()
    
    try:
        ResourceFile.objects.get(resource=resource, pk=file_id).delete()
    except ResourceFile.DoesNotExist:
        pass
    
    return HttpResponseRedirect(reverse('orb_resource_create2', args=[id])) 

def resource_create_url_delete_view(request, id, url_id):
    # check ownership
    try:
        resource = Resource.objects.get(pk=id)
    except Resource.DoesNotExist:
        raise Http404()
    if not resource_can_edit(resource, request.user):
        raise Http404()
    
    try:
        ResourceURL.objects.get(resource=resource, pk=url_id).delete()
    except ResourceURL.DoesNotExist:
        pass
    
    return HttpResponseRedirect(reverse('orb_resource_create2', args=[id])) 

def resource_edit_file_delete_view(request, id, file_id):
    # check ownership
    try:
        resource = Resource.objects.get(pk=id)
    except Resource.DoesNotExist:
        raise Http404()
    if not resource_can_edit(resource, request.user):
        raise Http404()
    
    try:
        ResourceFile.objects.get(resource=resource, pk=file_id).delete()
    except ResourceFile.DoesNotExist:
        pass
    
    return HttpResponseRedirect(reverse('orb_resource_edit2', args=[id])) 

def resource_edit_url_delete_view(request, id, url_id):
    # check ownership
    try:
        resource = Resource.objects.get(pk=id)
    except Resource.DoesNotExist:
        raise Http404()
    if not resource_can_edit(resource, request.user):
        raise Http404()
    
    try:
        ResourceURL.objects.get(resource=resource, pk=url_id).delete()
    except ResourceURL.DoesNotExist:
        pass
    
    return HttpResponseRedirect(reverse('orb_resource_edit2', args=[id])) 

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
    
    for k,v  in ResourceCriteria.CATEGORIES:
        #print k.get_category_display()
        print v
        obj = {}
        cat = ResourceCriteria.objects.filter(category=k).order_by('order_by')
        obj['category'] = cat[0].get_category_display()
        obj['category_order_by'] = cat[0].category_order_by
        obj['criteria'] = cat
        #obj['category'] = k.get_category_display()
        
        criteria.append(obj)
        
    return render_to_response('orb/resource/guidelines.html',
                              {'criteria_categories': criteria, 
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
        form.fields['criteria'].choices = [(t.id, t.description) for t in ResourceCriteria.objects.all().order_by('category_order_by','order_by')]
            
        if form.is_valid():
            resource.status = Resource.REJECTED
            resource.save()
            notes = form.cleaned_data.get("notes")
            criteria = form.cleaned_data.get("criteria")
            resource_workflow.send(sender=resource, resource=resource, request=request, status=ResourceWorkflowTracker.REJECTED, notes=notes, criteria=criteria)
            return HttpResponseRedirect(reverse('orb_resource_reject_sent', args=[resource.id]))
    else:
        form = ResourceRejectForm()
        form.fields['criteria'].choices = [(t.id, t.description) for t in ResourceCriteria.objects.all().order_by('category_order_by','order_by')]
        
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
            return HttpResponseRedirect(settings.MEDIA_URL + file.file.name)
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
        form = ResourceStep1Form(data = request.POST, files = request.FILES)
        resource_form_set_choices(form)
            
        if form.is_valid():
            resource.update_user = request.user
            resource.title = form.cleaned_data.get("title")
            resource.description = form.cleaned_data.get("description")
            if form.cleaned_data.get("study_time_number") and form.cleaned_data.get("study_time_unit"):
                resource.study_time_number = form.cleaned_data.get("study_time_number")
                resource.study_time_unit = form.cleaned_data.get("study_time_unit")
            resource.attribution = form.cleaned_data.get("attribution")
            resource.save()
                
            # update image
            image = form.cleaned_data.get("image")
            
            if image == False:
                resource.image = None
                resource.save()
            
            if request.FILES.has_key('image'):
                resource.image = request.FILES["image"]
                resource.save()
            
            
            
            # update tags - remove all current tags first
            ResourceTag.objects.filter(resource=resource).delete()
            resource_add_tags(request, form, resource)
            resource_add_free_text_tags(request, form, resource,'organisations','organisation')
            resource_add_free_text_tags(request, form, resource,'geography','geography')
            resource_add_free_text_tags(request, form, resource, 'languages','language')
            resource_add_free_text_tags(request, form, resource,'other_tags','other')
            
            # All successful - now redirect
            return HttpResponseRedirect(reverse('orb_resource_edit2', args=[resource.id])) # Redirect after POST
        else:
            initial = request.POST
            initial['image'] = resource.image
            files = ResourceFile.objects.filter(resource=resource)[:1]
            if files:
                initial['file'] = files[0].file
            form = ResourceStep1Form(initial = initial, data = request.POST, files = request.FILES)
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
        data['attribution'] = resource.attribution
        
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
        
        form = ResourceStep1Form(initial= data)
        resource_form_set_choices(form )
        
    return render_to_response('orb/resource/edit.html',
                              {'form': form, 
                               },
                              context_instance=RequestContext(request))
 
def resource_edit_step2_view(request, resource_id):
    if request.user.is_anonymous():
        return render_to_response('orb/login_required.html',
                              {'message': _(u'You need to be logged in to add a resource.') },
                              context_instance=RequestContext(request))
     
    try:
        resource = Resource.objects.get(pk=resource_id)
    except Resource.DoesNotExist:
        raise Http404()
       
    # check if owner of this resource
    if not resource_can_edit(resource, request.user):
        raise Http404()
    
    if request.method == 'POST':
        form = ResourceStep2Form(request.POST, request.FILES, request=request)
        
        if form.is_valid():
            title = form.cleaned_data.get("title")
            # add file and url
            if request.FILES.has_key('file'):
                rf = ResourceFile(resource=resource, create_user=request.user, update_user=request.user)
                rf.file=request.FILES["file"]
                if title:
                    rf.title = title
                rf.save()
            
            url = form.cleaned_data.get("url")
            if url:
                ru = ResourceURL(resource=resource, create_user=request.user, update_user=request.user) 
                ru.url = url
                if title:
                    ru.title = title
                ru.save()
        
    initial = {}
    form = ResourceStep2Form(initial=initial, request=request)
       
    resource_files = ResourceFile.objects.filter(resource=resource)
    resource_urls = ResourceURL.objects.filter(resource=resource)
    
    return render_to_response('orb/resource/edit_step2.html',
                              {'form': form, 
                               'resource': resource,
                               'resource_files': resource_files,
                               'resource_urls': resource_urls,
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

def search_view(request):
     
    search_query = request.GET.get('q', '')
    
    if search_query:
        search_results = SearchQuerySet().filter(content=search_query)
    else:
        search_results = []
        
    data = {}
    data['q'] = search_query
    form = SearchForm(initial=data)
     
    paginator = Paginator(search_results, settings.ORB_PAGINATOR_DEFAULT)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        results = paginator.page(page)
    except (EmptyPage, InvalidPage):
        results = paginator.page(paginator.num_pages)
     
    if search_query:
        search.send(sender=search_results, query=search_query, no_results=search_results.count(), request=request, page=page)
              
    return render_to_response('orb/search.html',
                              {'form': form, 
                               'query': search_query,
                               'page': results,
                               'total_results': paginator.count },
                              context_instance=RequestContext(request))
    

def search_advanced_view(request, tag_id=None):
      
    if request.method == 'POST':
        form = AdvancedSearchForm(request.POST)
        advanced_search_form_set_choices(form)
        if form.is_valid():
            urlparams = request.POST.copy()
            # delete these from params as not required
            del urlparams['csrfmiddlewaretoken']
            del urlparams['submit']
            return HttpResponseRedirect(reverse('orb_search_advanced_results') + "?" + urlparams.urlencode())
    else:
        data = {}
        if tag_id:
            tag = get_object_or_404(Tag, pk=tag_id)
            for name, slug in settings.ADVANCED_SEARCH_CATEGORIES:
                if tag.category.slug == slug:
                    data[name] = tag.id
        form = AdvancedSearchForm(initial=data)
        advanced_search_form_set_choices(form)

           
    return render_to_response('orb/search_advanced.html',
                              {'form': form, 
                               },
                              context_instance=RequestContext(request))

def search_advanced_results_view(request):
    
    form = AdvancedSearchForm(request.GET)
    advanced_search_form_set_choices(form)
    q = request.GET.get('q', '').strip()
    
    if form.is_valid():
        tag_ids = []
        for name, slug in settings.ADVANCED_SEARCH_CATEGORIES:
            for i in form.cleaned_data.get(name):
                tag_ids.append(i)
        resource_tags = ResourceTag.objects.filter(tag__pk__in=tag_ids).values('resource').annotate(dcount=Count('resource')).filter(dcount=len(tag_ids)).values('resource')
        
        licenses = form.cleaned_data.get('license')
        print licenses
        licenses_exclude = ResourceTag.objects.filter(tag__tagproperty__name='feature:shortname', tag__tagproperty__value__in=licenses).values('resource')
        print licenses_exclude
        
        if q == '' and len(resource_tags)  > 0:
            results = Resource.objects.filter(pk__in=resource_tags, status=Resource.APPROVED).exclude(pk__in=licenses_exclude)
        elif q != '' and len(resource_tags)  > 0:
            search_results = SearchQuerySet().filter(content=q).models(Resource).values_list('pk', flat=True)
            results = Resource.objects.filter(pk__in=resource_tags, status=Resource.APPROVED).filter(pk__in=search_results).exclude(pk__in=licenses_exclude)
        elif q != '' and len(resource_tags) == 0: 
            search_results = SearchQuerySet().filter(content=q).models(Resource).values_list('pk', flat=True)
            results = Resource.objects.filter(pk__in=search_results, status=Resource.APPROVED).exclude(pk__in=licenses_exclude)
        elif q == '' and len(resource_tags) == 0 and len(licenses_exclude) == 0: 
            results = Resource.objects.none()
        elif q == '' and len(resource_tags) == 0 and len(licenses_exclude) > 0:
            results = Resource.objects.filter(status=Resource.APPROVED).exclude(pk__in=licenses_exclude)
            
        paginator = Paginator(results, settings.ORB_PAGINATOR_DEFAULT)
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
        
        search.send(sender=results, query=q, no_results=results.count(), request=request, type=SearchTracker.SEARCH_ADV, page=page)
    else:
        filter_tags = Tag.objects.filter(pk=None)
        resources = Resource.objects.filter(pk=None)
        licenses = None
        paginator = Paginator(resources, settings.ORB_PAGINATOR_DEFAULT)
        
    return render_to_response('orb/search_advanced_results.html',
                              { 'filter_tags': filter_tags,
                               'license_tags': licenses,
                               'q': q,
                               'page': resources,
                               'total_results': paginator.count },
                              context_instance=RequestContext(request))

def tag_link_view(request, id):
    try:
        tag = Tag.objects.get(pk=id)
        
        tag_viewed.send(sender=tag, tag=tag, request=request, data=tag.external_url, type=TagTracker.VIEW_URL)
        return HttpResponseRedirect(tag.external_url)
    except Tag.DoesNotExist:
        raise Http404()


def collection_view(request,collection_slug):
    collection = Collection.objects.get(slug=collection_slug,visibility=Collection.PUBLIC)
    
    data = Resource.objects.filter(collectionresource__collection=collection, status=Resource.APPROVED).order_by('collectionresource__order_by')
    
    paginator = Paginator(data, settings.ORB_PAGINATOR_DEFAULT)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        resources = paginator.page(page)
    except (EmptyPage, InvalidPage):
        resources = paginator.page(paginator.num_pages)
    
    return render_to_response('orb/collection/view.html',
                              { 'collection': collection,
                               'page': resources,
                               'total_results': paginator.count },
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

def advanced_search_form_set_choices(form):
    for name, slug in settings.ADVANCED_SEARCH_CATEGORIES:
        form.fields[name].choices = [(t.id, t.name) for t in Tag.objects.filter(category__slug=slug, resourcetag__resource__status=Resource.APPROVED).distinct().order_by('order_by','name')]
        
    form.fields['license'].choices = [('ND','Derivatives allowed'), ('NC','Commerical use allowed')]
    return form 

def resource_can_view(resource, user):
    if resource.status == Resource.APPROVED:
        return True
    elif user.is_anonymous():
        return False
    elif ((user.is_staff or 
        user == resource.create_user or 
        user == resource.update_user) or
        (user.userprofile and (user.userprofile.crt_member == True or
        user.userprofile.mep_member == True))):
        return True 
    else:
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
