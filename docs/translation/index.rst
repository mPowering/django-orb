======================================================
Internationalization/Translations - Technical Set-up
======================================================

Translating source content
==========================

Todo. See the `Django i18n docs <https://docs.djangoproject.com/en/1.8/topics/i18n/>`_ in the meantime!


Translating database content
============================

Content in the database is user created content and cannot be translated using
the normal `gettext` interface that Django provides. Instead a package called
`django-modeltranslation <http://django-modeltranslation.readthedocs.io/en/latest/>`_
provides for language-specific *mirrored fields* in the database that allow for
content specific translation.

Specifying models and fields for translation
--------------------------------------------

Translations are *registered* much like `admin.ModelAdmin` classes in a
`translation.py` file in each app root. For each model to translate create a
translation class based on the `TranslationOptions` class, and specify the
fields.::

    from modeltranslation.translator import translator, TranslationOptions
    from orb import models

    class CategoryTranslation(TranslationOptions):
        fields = ('name',)

    translator.register(models.Category, CategoryTranslation)

In the above example the `CategoryTranslation` class specifies only that the
`name` field should be translated, and the `Category` model is registered with
this translation options class.

Realizing new translation fields
--------------------------------

Field registration is by itself an insufficient step. It is like adding new
fields to a model - you still need to create a database migration to realize
the field(s). This is straightforward 3-step process.

1. Run `makemigrations` for the app in question
2. Apply the migrations with `migrate`
3. Update the translation fields with the `update_translation_fields` command

The third step is important because of how `modeltranslations` pulls data out
of the database. If you have a `name` field and then decide to translate it,
then presuming an English language site with Spanish and Portuguese available
as well, you will have *four* database fields: `name`, `name_en`, `name_es`,
and `name_pt`.

.. note::
    Dialect or region specific codes will have their own fields if specified,
    e.g. `name_pt_br`.

Once active, `modeltranslation` will look for the `name` value in `name_en`!
Running `update_translation_fields` updates those values.

A convenience command has been added to the Makefile::

    make register-languages

This will create migrations, apply them, and then update the translation fields.

.. important::
    You must create new migrations any time you register new models/fields and
    also if you change the project `LANGUAGES` setting, so that database fields
    are available for each language.
