from django.db import models
from django.utils.translation import ugettext_lazy as _
from tinymce.models import HTMLField


class Toolkit(models.Model):
    """
    Provides an external link functionality
    """
    order_by = models.IntegerField(default=0)
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = HTMLField()
    uploaded_image = models.ImageField(blank=True, null=True)
    external_image = models.CharField(blank=True, null=True, max_length=1000)

    class Meta:
        ordering = ('order_by',)
        verbose_name = _("toolkit")
        verbose_name_plural = _("toolkits")

    def __unicode__(self):
        return self.title

    @property
    def image_path(self):
        try:
            return self.uploaded_image.url
        except ValueError:
            return self.external_image
