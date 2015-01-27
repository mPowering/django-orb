import datetime
from haystack import indexes
from mpowering.models import Resource, Organisation


class ResourceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='create_user')
    #create_date = indexes.DateTimeField(model_attr='create_date')

    def get_model(self):
        return Resource

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(status=Resource.APPROVED)
    
 
'''   
class OrganisationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='create_user')
    #create_date = indexes.DateTimeField(model_attr='create_date')

    def get_model(self):
        return Organisation

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
'''