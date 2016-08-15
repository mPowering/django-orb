from django.apps import AppConfig
from django.db.models.signals import post_save


class ORBConfig(AppConfig):
    name = 'orb'
    verbose_name = "ORB"

    def ready(self):
        from orb import callbacks
        Resource = self.get_model('Resource')
        post_save.connect(callbacks.resource_submitted_callback, sender=Resource)
