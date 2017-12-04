

def is_search_crawler(user_agent):
    spiders = { 'bot',
                'crawl',
                'slurp',
                'spider',
                'archiver',
                'facebook',
               'Lycos',
               'Scooter',
               'AltaVista',
               'Teoma',
               'domainreanimator.com',
               'Python-urllib',
               'YandexImages',
               'Plukkie',
               'BuzzSumo',
               'Clickagy',
               'Kraken',
               'Wotbox',
               'Nutch',
               'ContextAd',
               'Pinterest',
               'DeuSu',   
               'Go-http-client',
               'Yeti',
               'ltx71',
               'qwantify',
               }
    for s in spiders:
        if s.lower() in user_agent.lower():
            return True
    return False
