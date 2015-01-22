def modify(settings):
    
    settings['INSTALLED_APPS'] += ('crispy_forms', 'tastypie', 'tinymce', 'django_wysiwyg',)
    settings['TEMPLATE_CONTEXT_PROCESSORS'] += ('mpowering.context_processors.get_menu',)
    settings['CRISPY_TEMPLATE_PACK'] = 'bootstrap3'
    settings['SHOW_GRAVATARS'] = True
    settings['MPOWERING_GOOGLE_ANALYTICS_CODE'] = 'UA-58593028-1'
    
    settings['TASK_UPLOAD_FILE_TYPES'] = ['pdf', 'vnd.oasis.opendocument.text','vnd.ms-excel','msword','application',]
    settings['TASK_UPLOAD_FILE_MAX_SIZE'] = "5242880"
    settings['DJANGO_WYSIWYG_FLAVOR'] = "tinymce_advanced"
