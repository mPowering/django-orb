
from django.db import models
from django.utils.translation import ugettext_lazy as _

from orb.lib.unique_slugify import unique_slugify

# CountryData


class CountryData(models.Model):
    country_name = models.TextField(blank=False, null=False)
    slug = models.CharField(blank=True, null=True, max_length=100)
    country_code = models.TextField(blank=False, null=False)
    no_children_under5 = models.BigIntegerField(null=True, blank=True)
    no_chw = models.BigIntegerField(null=True, blank=True)
    pop_est = models.BigIntegerField(null=True, blank=True)
    no_childbearing_age = models.BigIntegerField(null=True, blank=True)
    fertility_rate = models.DecimalField(
        null=True, blank=True, max_digits=6, decimal_places=2)
    under5_mortality = models.IntegerField(null=True, blank=True)
    last_census_year = models.IntegerField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('CountryData')
        verbose_name_plural = _('CountryData')
        ordering = ('country_name',)

    def __unicode__(self):
        return self.country_name

    def save(self, *args, **kwargs):
        self.country_name = self.country_name.strip()
        unique_slugify(self, self.country_name)
        super(CountryData, self).save(*args, **kwargs)
