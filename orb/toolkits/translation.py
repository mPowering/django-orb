"""
Translation registration for django modeltranslation
"""

from modeltranslation.translator import translator, TranslationOptions

from orb.toolkits import models


class ToolkitTranslation(TranslationOptions):
    fields = ('title', 'description')


translator.register(models.Toolkit, ToolkitTranslation)
