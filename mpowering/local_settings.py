def modify(settings):
    
    settings['INSTALLED_APPS'] += ('crispy_forms', 'tastypie',)
    settings['TEMPLATE_CONTEXT_PROCESSORS'] += ('mpowering.context_processors.get_menu',)
    settings['CRISPY_TEMPLATE_PACK'] = 'bootstrap3'
    settings['SHOW_GRAVATARS'] = True
    settings['MPOWERING_GOOGLE_ANALYTICS_CODE'] = 'UA-58593028-1'
